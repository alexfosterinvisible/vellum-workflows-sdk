Below is a more human-readable, organized summary of the OpenAPI specification. It provides an overview of each endpoint, its purpose, the request parameters, request and response schemas, and the expected behavior. This is not a direct JSON or YAML copy but rather a structured interpretation meant to be more easily understood.

---

## Two Pi R Quality SDK (Version 0.0.1)

**Description:**  
2 Pi R provides quality components useful for delivering impactful, useful generative AI applications.

**Base URL:**  
`/v1`

**Contact:**  
Developer contact details not provided here.

**License:**  
Apache 2.0

---

## Endpoints Overview

### Contracts

- **POST** `/contracts/generate_dimensions`: Generate dimensions for a contract  
  **Request Body (application/json):**
  ```json
  {
    "contract": {
      "name": "string",
      "description": "string",
      "dimensions": []
    }
  }
  ```
  
  **Response (200):** A contract with populated dimensions
  ```json
  {
    "name": "string",
    "description": "string",
    "dimensions": []
  }
  ```

  **Response (422):** Validation error structure.
  
- **POST** `/contracts/score`: Score a contract given an input and output  
  **Request Body (application/json):**
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
  
  **Response (200):** Score details
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
  
  **Response (403):** `{"detail": "Not authenticated"}`  
  **Response (422):** Validation error structure.

### Feedback

- **POST** `/feedback/cluster`: Cluster feedback into groups with counts  
  **Request Body (application/json):**
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
  
  **Response (200):** Clusters with counts
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

  **Response (422):** Validation error structure.

### Inputs (Data)

- **POST** `/data/input/cluster`: Cluster input data into groups with counts  
  **Request Body (application/json):**
  ```json
  [
    {
      "identifier": "string",
      "llm_input": "string"
    }
  ]
  ```
  
  **Response (200):**
  ```json
  [
    {
      "topic": "string",
      "inputs": ["input_id"]
    }
  ]
  ```
  
  **Response (422):** Validation error structure.

- **POST** `/data/input/generate_from_seeds?num_inputs=<int>`: Generate input data from seeds  
  **Query Param:** `num_inputs` (integer, required)
  
  **Request Body (application/json):**
  ```json
  [
    "string"
  ]
  ```
  
  **Response (200):** Data generation status
  ```json
  {
    "state": "queued",
    "detailed_status": ["string"],
    "job_id": "string",
    "data": ["string"]
  }
  ```
  
  **Response (422):** Validation error structure.

- **GET** `/data/input/generate_from_seeds/{job_id}`: Check status of a data generation job  
  **Path Param:** `job_id` (string, required)
  
  **Response (200):** Data generation status (same schema as above).
  
  **Response (422):** Validation error structure.

- **GET** `/data/input/generate_from_seeds/{job_id}/messages`: Stream messages from the data generation job  
  **Path Param:** `job_id` (string, required)
  
  **Response (200):** Streaming text/plain messages.  
  **Response (422):** Validation error structure.

- **POST** `/data/input/evaluate`: Evaluate an input against a contract  
  **Request Body (application/json):**
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
  
  **Response (200):**
  ```json
  {
    "filter_score": 0
  }
  ```
  
  **Response (422):** Validation error structure.

- **POST** `/data/input/generate_seeds`: Generate seed messages for input data  
  **Request Body (application/json):**
  ```json
  {
    "contract": {
      "name": "string",
      "description": "string",
      "dimensions": []
    },
    "num_inputs": 0,
    "context_types": ["none"]
  }
  ```
  
  **Response (200):** Data generation status (same schema as above).  
  **Response (422):** Validation error structure.

### Inference

- **POST** `/inference/run`: Run LLM inference on an input  
  **Request Body (application/json):**
  ```json
  {
    "model_id": "gpt_4o_mini_agent",
    "llm_input": "string"
  }
  ```
  
  **Response (200):**
  ```json
  {
    "text": "string",
    "structured": {}
  }
  ```
  
  **Response (422):** Validation error structure.

### Prompts (Tuning)

- **POST** `/tune/prompt`: Start a prompt optimization job  
  **Request Body (application/json):**
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
  
  **Response (200):** Tuning job status
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
  
  **Response (422):** Validation error structure.

- **GET** `/tune/prompt/{job_id}`: Check status of a prompt optimization job  
  **Path Param:** `job_id` (string, required)

  **Response (200):** Optimization status (same schema as above).
  
  **Response (422):** Validation error structure.

- **GET** `/tune/prompt/{job_id}/messages`: Stream messages about a prompt optimization job  
  **Path Param:** `job_id` (string, required)
  
  **Response (200):** Plain text streaming messages.  
  **Response (422):** Validation error structure.

---

## Common Response Structures

**Validation Error (422):**  
```json
{
  "detail": [
    {
      "loc": ["string", 0],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

**Data Generation Status:**  
```json
{
  "state": "queued" | "running" | "done" | "error",
  "detailed_status": ["string"],
  "job_id": "string",
  "data": ["string"] // present only if done
}
```

**Score Metrics (for contracts):**  
```json
{
  "total_score": number,
  "dimension_scores": {
    "dimensionName": {
      "total_score": number,
      "subdimension_scores": {
        "subdimName": number
      }
    }
  }
}
```

**Contract Schema:**  
Contracts and dimensions typically have the following structure:
```json
{
  "name": "string",
  "description": "string",
  "dimensions": [
    {
      "label": "string",
      "description": "string",
      "weight": number,
      "sub_dimensions": [
        {
          "label": "string",
          "description": "string",
          "scoring_type": "PI_SCORER" | "HUGGINGFACE_SCORER" | "PYTHON_CODE",
          "python_code": "string or null",
          "parameters": [number or null],
          "weight": number,
          "huggingface_url": "string or null",
          "action_dimension": null or nested subdimension,
          "action_on_low_score": boolean
        }
      ],
      "action_dimension": null or nested,
      "action_on_low_score": boolean
    }
  ]
}
```

---

This reformatted outline should provide a clearer understanding of the API endpoints, their inputs, and their outputs compared to the raw Swagger/OpenAPI documentation listed above.