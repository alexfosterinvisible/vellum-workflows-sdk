# Prompts API

## Overview
The Prompts API allows you to execute and manage prompt deployments, handle streaming responses, and submit feedback.

## Endpoints

### Execute Prompt (GA)
```http
POST https://predict.vellum.ai/v1/execute-prompt
```

Executes a deployed Prompt and returns the result.

#### Request
```json
{
  "inputs": [
    {
      "type": "string",
      "name": "input_name",
      "value": "input_value"
    }
  ],
  "prompt_deployment_id": "string",
  "prompt_deployment_name": "string",
  "release_tag": "string",
  "external_id": "string",
  "expand_meta": {},
  "metadata": {}
}
```

#### Response
```json
{
  "id": "execution_id",
  "outputs": {
    "completion": "Generated response",
    "tokens": 150,
    "finish_reason": "stop"
  },
  "meta": {
    "prompt_version_id": "version_id",
    "model_params": {}
  }
}
```

### Execute Prompt Stream (GA)
```http
POST https://predict.vellum.ai/v1/execute-prompt-stream
```

Streams back results from a deployed Prompt.

#### Stream Events
```json
// Initiated Event
{
  "type": "INITIATED",
  "execution_id": "string",
  "timestamp": "2024-01-15T09:30:00Z"
}

// Streaming Event
{
  "type": "STREAMING",
  "execution_id": "string",
  "delta": "partial response",
  "timestamp": "2024-01-15T09:30:01Z"
}

// Fulfilled Event
{
  "type": "FULFILLED",
  "execution_id": "string",
  "final_output": "complete response",
  "timestamp": "2024-01-15T09:30:02Z"
}
```

### Submit Prompt Execution Actuals (GA)
```http
POST https://predict.vellum.ai/v1/submit-completion-actuals
```

Submit feedback about prompt execution quality.

#### Request
```json
{
  "actuals": [
    {
      "execution_id": "string",
      "rating": 1,
      "feedback": "Good response",
      "metadata": {}
    }
  ]
}
```

## Client Examples

### Python
```python
from vellum import Client

client = Client(api_key="your-api-key")

# Execute prompt
response = client.execute_prompt(
    prompt_deployment_name="my-prompt",
    inputs=[{"name": "query", "value": "Hello!"}]
)

# Stream response
async for event in client.execute_prompt_stream(
    prompt_deployment_name="my-prompt",
    inputs=[{"name": "query", "value": "Hello!"}]
):
    print(event.delta)

# Submit feedback
client.submit_completion_actuals(
    actuals=[{
        "execution_id": "exec_id",
        "rating": 1
    }]
)
```

### TypeScript
```typescript
import { Client } from '@vellum-ai/client';

const client = new Client({ apiKey: 'your-api-key' });

// Execute prompt
const response = await client.executePrompt({
  promptDeploymentName: 'my-prompt',
  inputs: [{ name: 'query', value: 'Hello!' }]
});

// Stream response
for await (const event of client.executePromptStream({
  promptDeploymentName: 'my-prompt',
  inputs: [{ name: 'query', value: 'Hello!' }]
})) {
  console.log(event.delta);
}

// Submit feedback
await client.submitCompletionActuals({
  actuals: [{
    executionId: 'exec_id',
    rating: 1
  }]
});
```

## Best Practices

### Error Handling
```python
try:
    response = client.execute_prompt(...)
except VellumError as e:
    if e.code == "RATE_LIMITED":
        # Implement backoff
    elif e.code == "INVALID_INPUT":
        # Handle input validation
    else:
        # Handle other errors
```

### Streaming
1. Use streaming for long responses
2. Handle connection drops
3. Implement timeout logic
4. Buffer partial responses

### Feedback
1. Submit feedback promptly
2. Include relevant metadata
3. Use consistent rating scale
4. Track feedback patterns

## Rate Limits
- Standard tier: 10 requests/second
- Enterprise tier: Custom limits
- Implement exponential backoff
- Monitor usage metrics

## Support
- [API Reference](https://docs.vellum.ai/api)
- [Examples](https://github.com/vellum-ai/examples)
- [Support](https://support.vellum.ai)
``` 