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

### Phase 2: Core Functionality (Building Understanding)
1. **Contract Structure**
   - Generate dimensions from simple contract
   - Test scoring with generated dimensions
   - Try Python code execution
   - REASON: Contracts seem central to system

2. **Data Generation**
   - Generate basic seeds
   - Test input generation
   - Validate clustering
   - REASON: Need data for deeper testing

3. **Feedback Flow**
   - Test clustering with known inputs
   - Try different rating values
   - Check source options
   - REASON: Understanding quality metrics

### Phase 3: Advanced Features (Completing the Picture)
1. **Prompt Tuning**
   - Test basic tuning
   - Try different algorithms
   - Monitor convergence
   - REASON: Most complex feature, needs other pieces first

2. **Integration Points**
   - Test action triggers
   - Try batch operations
   - Validate error handling
   - REASON: Can only test after understanding core flows

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

## Next Steps

1. Implement Probe 1:
   - Focus on auth, rate limits, basic endpoints
   - Run tests in parallel with rate limiting
   - Save full responses for analysis

2. Analyze Results:
   - Look for patterns in responses
   - Note any unexpected behaviors
   - Update hypotheses based on findings

3. Plan Probe 2:
   - Adjust based on Probe 1 results
   - Focus on most promising paths
   - Design more complex test cases

## Questions to Answer First

1. Authentication:
   - How does rate limiting work?
   - Are there different API key types?
   - What happens at the limits?

2. Basic Operations:
   - What's the minimal valid contract?
   - How fast is inference?
   - What's the job lifecycle?

3. Data Requirements:
   - What makes a valid input?
   - How are IDs generated?
   - What are the size limits?

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
