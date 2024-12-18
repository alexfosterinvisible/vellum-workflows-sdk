# Test Suites API

## Overview
The Test Suites API enables you to manage test cases, execute test runs, and analyze results for your prompts and workflows.

## Endpoints

### List Test Cases (Beta)
```http
GET https://api.vellum.ai/v1/test-suites/:id/test-cases
```

List test cases associated with a test suite.

#### Parameters
- `limit`: Results per page
- `offset`: Pagination offset

#### Response
```json
{
  "count": 50,
  "results": [
    {
      "id": "test_123",
      "label": "Basic Query Test",
      "input_values": [
        {
          "name": "query",
          "value": "test input"
        }
      ],
      "evaluation_values": [
        {
          "name": "expected_output",
          "value": "expected result"
        }
      ]
    }
  ]
}
```

### Upsert Test Cases (Beta)
```http
POST https://api.vellum.ai/v1/test-suites/:id/test-cases
```

Create or update test cases in a test suite.

#### Request
```json
{
  "input_values": [
    {
      "name": "query",
      "value": "test input"
    }
  ],
  "evaluation_values": [
    {
      "name": "expected_output",
      "value": "expected result"
    }
  ],
  "label": "Basic Query Test",
  "external_id": "test_123"
}
```

### Create Test Suite Run (Beta)
```http
POST https://api.vellum.ai/v1/test-suite-runs
```

Trigger a test suite execution.

#### Request
```json
{
  "test_suite_id": "suite_123",
  "exec_config": {
    "type": "EXTERNAL",
    "data": {
      "executions": [
        {
          "test_case_id": "test_123",
          "outputs": [
            {
              "name": "result",
              "type": "STRING"
            }
          ]
        }
      ]
    }
  }
}
```

## Client Examples

### Python
```python
from vellum import Client

client = Client(api_key="your-api-key")

# List test cases
cases = client.list_test_cases(
    test_suite_id="suite_123",
    limit=10
)

# Create test case
case = client.upsert_test_case(
    test_suite_id="suite_123",
    input_values=[{
        "name": "query",
        "value": "test input"
    }],
    evaluation_values=[{
        "name": "expected_output",
        "value": "expected result"
    }],
    label="Basic Query Test"
)

# Run test suite
run = client.create_test_suite_run(
    test_suite_id="suite_123",
    exec_config={
        "type": "EXTERNAL",
        "data": {
            "executions": [{
                "test_case_id": "test_123",
                "outputs": [{
                    "name": "result",
                    "type": "STRING"
                }]
            }]
        }
    }
)

# Get run results
results = client.list_test_suite_executions(
    test_suite_run_id=run.id
)
```

### TypeScript
```typescript
import { Client } from '@vellum-ai/client';

const client = new Client({ apiKey: 'your-api-key' });

// List test cases
const cases = await client.listTestCases({
  testSuiteId: 'suite_123',
  limit: 10
});

// Create test case
const case = await client.upsertTestCase({
  testSuiteId: 'suite_123',
  inputValues: [{
    name: 'query',
    value: 'test input'
  }],
  evaluationValues: [{
    name: 'expected_output',
    value: 'expected result'
  }],
  label: 'Basic Query Test'
});

// Run test suite
const run = await client.createTestSuiteRun({
  testSuiteId: 'suite_123',
  execConfig: {
    type: 'EXTERNAL',
    data: {
      executions: [{
        testCaseId: 'test_123',
        outputs: [{
          name: 'result',
          type: 'STRING'
        }]
      }]
    }
  }
});

// Get run results
const results = await client.listTestSuiteExecutions({
  testSuiteRunId: run.id
});
```

## Best Practices

### Test Case Design
1. Input Coverage
   - Test edge cases
   - Include common scenarios
   - Vary input complexity
   - Test input validation

2. Evaluation Criteria
   - Define clear expectations
   - Use consistent metrics
   - Include validation rules
   - Set score thresholds

3. Test Organization
   - Group related tests
   - Use descriptive labels
   - Add detailed metadata
   - Maintain test hygiene

### Test Execution
1. Run Configuration
   - Set appropriate timeouts
   - Configure retry logic
   - Handle failures gracefully
   - Monitor execution status

2. Results Analysis
   - Track success rates
   - Analyze failure patterns
   - Monitor performance
   - Generate reports

## Rate Limits
- Test case operations: 10 requests/second
- Test runs: 2 runs/second
- Results retrieval: 20 requests/second
- Enterprise: Custom limits

## Support
- [API Reference](https://docs.vellum.ai/api/test-suites)
- [Examples](https://github.com/vellum-ai/examples)
- [Support](https://support.vellum.ai) 