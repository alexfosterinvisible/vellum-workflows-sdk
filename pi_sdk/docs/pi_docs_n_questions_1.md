# Two Pi R Quality SDK Documentation with Questions

## Base Information
Base URL: `/v1`
License: Apache 2.0

## Endpoints and Questions

### Contracts

#### POST `/contracts/generate_dimensions`
**Questions:**
- What makes a good contract description? Examples?
- How specific should the contract name be?
- What's the relationship between name and description in terms of dimension generation?
- How are the generated dimensions influenced by the input text?
- Do certain words/phrases trigger specific dimension types?

**Request:**
```json
{
  "contract": {
    "name": "string",
    "description": "string",
    "dimensions": []
  }
}
```

**Response:**
```json
{
  "name": "string",
  "description": "string",
  "dimensions": []
}
```

**Questions about Response:**
- What's the typical number of dimensions generated?
- Are dimensions hierarchical or flat?
- How are weights assigned to generated dimensions?
- Can we expect consistent dimensions for similar contracts?

#### POST `/contracts/score`
**Questions:**
- What constitutes a good `llm_input`? Examples?
- How should `llm_output` relate to input?
- Are there length limits/requirements for input/output?
- What's the relationship between contract dimensions and scoring?

**Request:**
```json
{
  "contract": {
    "name": "string",
    "description": "string",
    "dimensions": []
  },
  "llm_input": "string",
  "llm_output": "string"
}
```

**Response:**
```json
{
  "total_score": 0,
  "dimension_scores": {
    "dimensionName": {
      "total_score": 0,
      "subdimension_scores": {
        "subdimName": 0
      }
    }
  }
}
```

**Questions about Response:**
- What's the score range? (0-1, 0-100?)
- How should we interpret different score ranges?
- Are subdimension scores weighted in total_score?
- What's a "good" vs "bad" score?

### Feedback

#### POST `/feedback/cluster`
**Questions:**
- What makes good feedback text in `comment`?
- How specific should the `identifier` be?
- How does input/output context affect clustering?
- What determines cluster boundaries?

**Request:**
```json
[
  {
    "identifier": "string",
    "llm_input": "string",
    "llm_output": "string",
    "comment": "string",
    "rating": "positive",
    "source": "internal"
  }
]
```

**Response:**
```json
[
  {
    "topic": "string",
    "rating": "positive",
    "per_source_counts": {
      "someSource": 0
    },
    "feedback": ["feedback_id"]
  }
]
```

**Questions about Response:**
- How are topics named/generated?
- What determines topic granularity?
- How reliable are the clusters?
- What's the relationship between topics and ratings?

### Inputs (Data)

#### POST `/data/input/cluster`
**Questions:**
- How should inputs be structured for best clustering?
- What makes inputs similar enough to cluster?
- Is there an optimal input length?

**Request:**
```json
[
  {
    "identifier": "string",
    "llm_input": "string"
  }
]
```

**Response:**
```json
[
  {
    "topic": "string",
    "inputs": ["input_id"]
  }
]
```

**Questions about Response:**
- How do these topics differ from feedback topics?
- What determines cluster size?
- Are topics hierarchical?

#### POST `/data/input/generate_from_seeds`
**Questions:**
- What makes a good seed?
- How diverse should seeds be?
- Should seeds be related to each other?
- What's the relationship between seed and generated inputs?

**Request:**
```json
[
  "string"
]
```

**Response:**
```json
{
  "state": "queued",
  "detailed_status": ["string"],
  "job_id": "string",
  "data": ["string"]
}
```

#### POST `/data/input/evaluate`
**Questions:**
- How does input evaluation relate to contract scoring?
- What makes an input "good" for a contract?
- How should inputs be structured for best evaluation?

**Request:**
```json
{
  "contract": {
    "name": "string",
    "description": "string",
    "dimensions": []
  },
  "llm_input": "string"
}
```

**Response:**
```json
{
  "filter_score": 0
}
```

**Questions about Response:**
- What's the filter_score range?
- How does it relate to contract scores?
- What threshold indicates a "good" input?

### Inference

#### POST `/inference/run`
**Questions:**
- What's the expected input format for each model?
- How should inputs be structured?
- Are there model-specific formatting requirements?
- What affects output quality?

**Request:**
```json
{
  "model_id": "gpt_4o_mini_agent",
  "llm_input": "string"
}
```

**Response:**
```json
{
  "text": "string",
  "structured": {}
}
```

**Questions about Response:**
- What determines structured vs text response?
- How reliable is the structured output?
- What schemas can we expect in structured?

### Prompts (Tuning)

#### POST `/tune/prompt`
**Questions:**
- What makes good tuning examples?
- How diverse should examples be?
- How do examples affect tuning quality?
- What's the relationship between examples and contract?

**Request:**
```json
{
  "contract": {
    "name": "string",
    "description": "string",
    "dimensions": []
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

**Response:**
```json
{
  "state": "queued",
  "detailed_status": ["string"],
  "job_id": "string",
  "contract": {
    "name": "string",
    "description": "string",
    "dimensions": []
  }
}
```

**Questions about Response:**
- What status messages can we expect?
- How do we know tuning is improving?
- What indicates successful tuning?

## Common Patterns Questions
1. Input Content:
   - Are there common patterns for good inputs?
   - Should inputs follow specific formats?
   - How do different endpoints interpret similar inputs?

2. Output Interpretation:
   - How should we interpret scores across different endpoints?
   - What patterns indicate success vs failure?
   - How reliable are the generated outputs?

3. Error Cases:
   - What makes inputs invalid?
   - How to handle malformed outputs?
   - What are common failure patterns?

4. Content Relationships:
   - How do contracts relate to tuning?
   - How do clusters relate to scoring?
   - How do examples influence generation? 