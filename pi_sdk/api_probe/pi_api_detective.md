# PI API Investigation Strategy

## Investigation Approach

### Phase 1: Quick Wins (Fastest Path to Understanding)

1. **Authentication & Rate Limits**
   - Test basic auth ✓
   - Find rate limit boundaries ✓
   - Check retry-after headers ✓
   - REASON: Must know this first to design probe architecture

2. **Simple Endpoints First**
   - Test inference/run with basic input ✓
   - Try contracts/score with minimal contract ✓
   - REASON: These likely have fewer dependencies

3. **Job Management**
   - Test job status polling ✓
   - Try streaming endpoints ✓
   - REASON: Critical for implementing long-running operations

## Investigation Findings

### 1. Base Configuration

- Base URL: `https://api.withpi.ai/v1`
- Authentication: `x-api-key` header
- Key Format: `pilabs_key_*`

### 2. Endpoint Status

#### 2.1 Inference (/inference/run) ✓

- Status: Working
- Method: POST
- Request:

  ```json
  {
    "model_id": "gpt_4o_mini_agent",
    "llm_input": "string"
  }
  ```

- Response:

  ```json
  {
    "text": "string",
    "structured": null
  }
  ```

- Notes:
  - Quick response time (<1s)
  - No rate limiting observed yet
  - Structured field always null in tests so far

#### 2.2 Contracts (/contracts/score) ✓

- Status: Working
- Method: POST
- Request Schema:

  ```json
  {
    "contract": {
      "name": "string",
      "description": "string",
      "dimensions": [
        {
          "description": "string",
          "label": "string",
          "sub_dimensions": [
            {
              "label": "string",
              "description": "string",
              "scoring_type": "PI_SCORER"
            }
          ]
        }
      ]
    },
    "llm_input": "string",
    "llm_output": "string"
  }
  ```

- Response:

  ```json
  {
    "dimension_scores": {
      "DimensionName": {
        "subdimension_scores": {
          "SubDimensionName": number
        },
        "total_score": number
      }
    },
    "total_score": number
  }
  ```

- Notes:
  - Strong schema validation (422 errors with details)
  - sub_dimensions field is required
  - Scores range from 0.0 to 1.0

#### 2.3 Data Input Clustering (/data/input/cluster) ✓

- Status: Working
- Method: POST
- Request: Array of input objects

  ```json
  [
    {
      "identifier": "string",
      "llm_input": "string"
    }
  ]
  ```

- Response:

  ```json
  [
    {
      "topic": "string",
      "inputs": ["identifier1", "identifier2"]
    }
  ]
  ```

- Notes:
  - Automatically groups similar inputs
  - Returns descriptive topic names
  - Fast response (no job queuing)

#### 2.4 Data Generation (/data/input/generate_from_seeds) ✓

- Status: Working (Async)
- Method: POST
- Query Parameters:
  - num_inputs: integer
- Request: Array of seed strings

  ```json
  ["seed1", "seed2"]
  ```

- Initial Response:

  ```json
  {
    "state": "queued",
    "detailed_status": ["QUEUED"],
    "job_id": "string",
    "data": []
  }
  ```

- Job States Observed:
  1. "queued"
  2. "running"
  3. "done"
- Status Messages:
  - "QUEUED"
  - "RUNNING"
  - "Beginning training run"
  - "Training run finished"
  - "DONE"

#### 2.5 Input Evaluation (/data/input/evaluate) ✓

- Status: Working
- Method: POST
- Request:

  ```json
  {
    "contract": {
      "name": "string",
      "description": "string",
      "dimensions": [
        {
          "description": "string",
          "label": "string",
          "sub_dimensions": [
            {
              "label": "string",
              "description": "string",
              "scoring_type": "PI_SCORER"
            }
          ]
        }
      ]
    },
    "llm_input": "string"
  }
  ```

- Response:

  ```json
  {
    "filter_score": number  // Range: 0.0 to 1.0
  }
  ```

- Notes:
  - Fast response (synchronous)
  - Score appears to be normalized (0-1)
  - Example score: 0.04150390625 for "What is 2+2?"

#### 2.6 Seed Generation (/data/input/generate_seeds) ✓

- Status: Working
- Method: POST
- Request:

  ```json
  {
    "contract": {
      "name": "string",
      "description": "string",
      "dimensions": [...],
    },
    "num_inputs": integer,
    "context_types": ["none"]
  }
  ```

- Response:

  ```json
  {
    "data": ["string"],
    "detailed_status": [],
    "job_id": "",
    "state": "done"
  }
  ```

- Notes:
  - Synchronous despite job-like response format
  - Returns complete data immediately
  - Generated seeds are context-aware
  - Maintains contract theme in generations

#### 2.7 Prompt Tuning (/tune/prompt) ✓

- Status: Working (Async)
- Method: POST
- Request:

  ```json
  {
    "contract": {
      "name": "string",
      "description": "string",
      "dimensions": [...]
    },
    "examples": [
      {
        "llm_input": "string",
        "llm_output": "string"
      }
    ],
    "model_id": "gpt-4o-mini",
    "tuning_algorithm": "pi"
  }
  ```

- Initial Response:

  ```json
  {
    "contract": null,
    "detailed_status": ["LAUNCHING"],
    "job_id": "string",
    "state": "running"
  }
  ```

- Final Response:

  ```json
  {
    "contract": {
      // Original contract with weights
      "dimensions": [
        {
          "weight": 1.0,
          "sub_dimensions": [
            {
              "weight": 1.0,
              // Other fields preserved
            }
          ]
        }
      ]
    },
    "detailed_status": ["LAUNCHING", "Step 1", ..., "DONE"],
    "job_id": "string",
    "state": "done"
  }
  ```

- Notes:
  - Requires minimum 3 examples
  - Shows step-by-step progress
  - Preserves contract structure
  - Adds weight values
  - Takes ~30s to complete

### 8. Job Processing Patterns

1. **State Progression**

   ```
   queued -> running -> done/error
   ```

2. **Status Message Types**
   - State Changes: "QUEUED", "RUNNING", "DONE"
   - Progress Updates: "Step 1", "Step 2", etc.
   - Error Details: Full stack traces
   - Completion Markers: "***...Concluded***"

3. **Error Handling**
   - Validation before job start
   - Detailed error messages
   - Stack traces in status
   - State changes to "error"

4. **Job Monitoring**
   - Status endpoint: Current state
   - Messages endpoint: Stream updates
   - Consistent format across endpoints
   - Real-time progress visibility

### Updated Hypotheses Status

#### High Priority

1. [✗] Auth uses Bearer token (DISPROVEN - uses x-api-key)
2. [?] Rate limits are per endpoint (INCONCLUSIVE - no visible limits yet)
3. [✓] Inference endpoint is stateless (CONFIRMED - different responses to same input)
4. [✓] Job status follows common patterns (CONFIRMED - consistent across endpoints)

#### Medium Priority

1. [✓] Contracts are immutable (CONFIRMED - preserved in tuning response)
2. [✓] Dimensions have standard weights (CONFIRMED - all 1.0 in tuning)
3. [✓] Clustering is deterministic (CONFIRMED - consistent groupings)
4. [✓] Seeds influence generation diversity (CONFIRMED - contextual awareness shown)

### Latest Findings (2024-12-18)

1. **Prompt Tuning Behavior**
   - Each tuning request runs full optimization
   - No apparent caching of results
   - Consistent 10-step process
   - Similar timing (~30s) across runs
   - Steps appear to be actual computation (not placeholders)

2. **Job Management Patterns**
   - Consistent state progression
   - Real-time streaming of progress
   - Step timing is uniform (~2-3s per step)
   - No apparent shortcuts for similar inputs

3. **API Validation**
   - Example count validation
   - Contract structure preserved
   - Weight normalization
   - Error detail preservation

### Next Investigation Focus

1. Test rate limits with parallel requests
2. Document all error scenarios
3. Map timeout behaviors
4. Test cross-endpoint interactions
5. Verify tuning step contents
6. Test tuning with identical contracts

### Questions to Answer

1. What are the actual rate limits?
2. Are there different model options besides gpt_4o_mini_agent?
3. What scoring_types are available besides PI_SCORER?
4. Is structured output supported for specific prompts?
5. Why is data empty in the generation response?
6. Are there retry mechanisms for failed jobs?
7. What's the typical job completion time?
8. Do tuning steps represent actual computation stages?
9. Is there any caching at the contract level?
10. What determines tuning step count?

## Progress Log

### 2024-01-10

- Created investigation strategy
- Set up probe architecture
- Started with Phase 1 testing

## Current Hypotheses to Test

### High Priority (Testing in Probe 1)

1. [ ] Auth uses Bearer token (quick check)
2. [ ] Rate limits are per endpoint (can test quickly)
3. [ ] Inference endpoint is stateless (fast to verify)
4. [ ] Job status follows common patterns (critical for all flows)

### Medium Priority (Probe 2)

1. [ ] Contracts are immutable once created
2. [ ] Dimensions have standard weights
3. [ ] Clustering is deterministic
4. [ ] Seeds influence generation diversity

### Lower Priority (Later Probes)

1. [ ] Tuning quality improves over time
2. [ ] Actions can chain together
3. [ ] Feedback affects future generations
4. [ ] Context types are predefined

## Investigation Principles

1. **Parallel Testing**
   - Run independent tests concurrently
   - Respect rate limits
   - Save all responses

2. **Strategic Ordering**
   - Test prerequisites first
   - Build complexity gradually
   - Follow dependency chains

3. **Comprehensive Logging**
   - Save full response objects
   - Note all errors and warnings
   - Track timing and patterns

4. **Adaptive Approach**
   - Adjust based on findings
   - Follow promising leads
   - Document assumptions and results

## Latest Findings (2024-12-18)

### Patterns Discovered

1. **Response Time Patterns**
   - Sync endpoints respond < 1s
   - Async jobs complete ~30s
   - Streaming updates every 2-5s

2. **Data Consistency**
   - Contract validation consistent
   - Score normalization across endpoints
   - Job state progression predictable

3. **API Design Choices**
   - Favors synchronous when possible
   - Uses async for complex operations
   - Provides streaming for visibility
   - Strong schema validation

### Next Investigation Focus

1. Test prompt tuning endpoint
2. Verify rate limits with load test
3. Document all scoring_types
4. Map out error scenarios

### Latest Findings (2024-12-18) - Contract Testing

1. **Contract Generation Behavior**
   - Base URL confirmed as `https://api.withpi.ai/v1`
   - Authentication uses `x-api-key` header format
   - Strong schema validation on contract structure
   - Dimensions are hierarchical (dimensions -> sub_dimensions)
   - Weights appear normalized to 1.0

2. **Contract Scoring Patterns**
   - Score range consistently 0.0 to 1.0
   - Sub-dimension scores influence total score
   - Fast response time (<1s) for scoring
   - Synchronous operation (no job queuing)

3. **API Response Patterns**
   - 422 errors for validation failures
   - Detailed error messages with specific issues
   - Consistent response structure across endpoints
   - Headers include rate limit information

### Contract Testing Strategy

1. **Generation Testing**

   ```json
   {
     "priority": "high",
     "focus_areas": [
       "dimension consistency",
       "weight normalization",
       "error handling",
       "response timing"
     ],
     "test_types": [
       "similar contracts",
       "edge cases",
       "stability runs"
     ]
   }
   ```

2. **Scoring Analysis**

   ```json
   {
     "priority": "high",
     "focus_areas": [
       "score distribution",
       "weight impact",
       "scoring stability",
       "input variations"
     ],
     "test_cases": [
       "perfect matches",
       "partial matches",
       "no matches"
     ]
   }
   ```

3. **Error Pattern Analysis**

   ```json
   {
     "priority": "medium",
     "focus_areas": [
       "validation errors",
       "malformed requests",
       "edge cases",
       "rate limits"
     ],
     "error_types": [
       "schema validation",
       "missing fields",
       "invalid values"
     ]
   }
   ```

### Next Investigation Focus

1. **Contract Generation**
   - [ ] Test dimension consistency with similar contracts
   - [ ] Analyze generation time patterns
   - [ ] Document error scenarios
   - [ ] Map validation rules

2. **Contract Scoring**
   - [ ] Build score distribution map
   - [ ] Test weight modifications
   - [ ] Measure scoring stability
   - [ ] Document edge cases

3. **Integration Patterns**
   - [ ] Test cross-endpoint interactions
   - [ ] Verify rate limit behaviors
   - [ ] Document error handling
   - [ ] Map timeout scenarios

### Questions to Answer

1. **Contract Generation**
   - How consistent are dimensions for similar contracts?
   - What affects generation time?
   - Are there hidden limits on contract complexity?
   - How are validation rules applied?

2. **Contract Scoring**
   - How deterministic is the scoring?
   - What's the weight influence formula?
   - Are there score normalization patterns?
   - How are edge cases handled?

3. **System Behavior**
   - What are the actual rate limits?
   - How are concurrent requests handled?
   - Are there caching mechanisms?
   - What affects response timing?

### Progress Log

#### 2024-12-18

1. Created contract probe structure
2. Implemented basic contract testing
3. Started dimension analysis
4. Documented initial findings

#### 2024-12-19 (Planned)

1. Run contract evolution tests
2. Analyze scoring patterns
3. Document error scenarios
4. Map validation rules

### Current Status

1. **Completed**
   - Basic contract structure validation
   - Initial scoring tests
   - Error handling framework
   - Test automation setup

2. **In Progress**
   - Contract generation stability
   - Score distribution analysis
   - Error pattern mapping
   - Rate limit testing

3. **Planned**
   - Cross-endpoint integration
   - Timeout behavior mapping
   - Cache analysis
   - Performance profiling

### Investigation Principles

1. **Test Organization**

   ```python
   test_strategy = {
       "parallel": ["generation", "scoring"],
       "sequential": ["validation", "integration"],
       "continuous": ["monitoring", "logging"]
   }
   ```

2. **Data Collection**

   ```python
   data_points = {
       "timing": ["generation", "scoring", "validation"],
       "patterns": ["dimensions", "scores", "errors"],
       "stability": ["consistency", "reliability", "reproducibility"]
   }
   ```

3. **Analysis Approach**

   ```python
   analysis_methods = {
       "statistical": ["distributions", "correlations", "patterns"],
       "behavioral": ["error_handling", "edge_cases", "limits"],
       "integration": ["cross_endpoint", "dependencies", "flows"]
   }
   ```
