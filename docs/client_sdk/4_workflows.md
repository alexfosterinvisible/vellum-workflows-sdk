# Workflows API

## Overview
The Workflows API enables you to execute and manage workflow deployments, handle streaming execution events, and submit feedback.

## Endpoints

### Execute Workflow (GA)
```http
POST https://predict.vellum.ai/v1/execute-workflow
```

Executes a deployed Workflow and returns its outputs.

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
  "workflow_deployment_id": "string",
  "workflow_deployment_name": "string",
  "release_tag": "string",
  "external_id": "string",
  "metadata": {}
}
```

#### Response
```json
{
  "execution_id": "string",
  "data": {
    "outputs": [
      {
        "name": "output_name",
        "value": "output_value",
        "type": "string"
      }
    ],
    "state": "FULFILLED"
  }
}
```

### Execute Workflow Stream (GA)
```http
POST https://predict.vellum.ai/v1/execute-workflow-stream
```

Streams back results from a deployed Workflow.

#### Stream Events
```json
// Workflow Event
{
  "type": "WORKFLOW",
  "execution_id": "string",
  "data": {
    "state": "INITIATED",
    "ts": "2024-01-15T09:30:00Z",
    "outputs": []
  }
}

// Node Event
{
  "type": "NODE",
  "execution_id": "string",
  "data": {
    "node_id": "string",
    "state": "RUNNING",
    "outputs": {}
  }
}
```

### Submit Workflow Execution Actuals (GA)
```http
POST https://predict.vellum.ai/v1/submit-workflow-execution-actuals
```

Submit feedback about workflow execution quality.

#### Request
```json
{
  "actuals": [
    {
      "execution_id": "string",
      "output_name": "result",
      "value": "Expected output",
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

# Execute workflow
response = client.execute_workflow(
    workflow_deployment_name="my-workflow",
    inputs=[{"name": "query", "value": "Process this"}]
)

# Stream execution
async for event in client.execute_workflow_stream(
    workflow_deployment_name="my-workflow",
    inputs=[{"name": "query", "value": "Process this"}],
    event_types=["WORKFLOW", "NODE"]
):
    if event.type == "WORKFLOW":
        print(f"Workflow state: {event.data.state}")
    elif event.type == "NODE":
        print(f"Node {event.data.node_id}: {event.data.state}")

# Submit feedback
client.submit_workflow_execution_actuals(
    actuals=[{
        "execution_id": "exec_id",
        "output_name": "result",
        "value": "Expected output"
    }]
)
```

### TypeScript
```typescript
import { Client } from '@vellum-ai/client';

const client = new Client({ apiKey: 'your-api-key' });

// Execute workflow
const response = await client.executeWorkflow({
  workflowDeploymentName: 'my-workflow',
  inputs: [{ name: 'query', value: 'Process this' }]
});

// Stream execution
for await (const event of client.executeWorkflowStream({
  workflowDeploymentName: 'my-workflow',
  inputs: [{ name: 'query', value: 'Process this' }],
  eventTypes: ['WORKFLOW', 'NODE']
})) {
  if (event.type === 'WORKFLOW') {
    console.log(`Workflow state: ${event.data.state}`);
  } else if (event.type === 'NODE') {
    console.log(`Node ${event.data.nodeId}: ${event.data.state}`);
  }
}

// Submit feedback
await client.submitWorkflowExecutionActuals({
  actuals: [{
    executionId: 'exec_id',
    outputName: 'result',
    value: 'Expected output'
  }]
});
```

## Best Practices

### Error Handling
```python
try:
    response = client.execute_workflow(...)
except VellumError as e:
    if e.code == "WORKFLOW_INITIALIZATION_ERROR":
        # Handle initialization errors
    elif e.code == "NODE_EXECUTION_ERROR":
        # Handle node-specific errors
    else:
        # Handle other errors
```

### Streaming
1. Monitor both workflow and node events
2. Handle connection interruptions
3. Implement timeout handling
4. Track node dependencies

### State Management
1. Use workflow state for coordination
2. Track node completion status
3. Handle parallel execution
4. Manage data dependencies

## Rate Limits
- Standard tier: 5 workflows/second
- Enterprise tier: Custom limits
- Consider node execution time
- Monitor parallel executions

## Support
- [API Reference](https://docs.vellum.ai/api/workflows)
- [Examples](https://github.com/vellum-ai/examples)
- [Support](https://support.vellum.ai)
``` 