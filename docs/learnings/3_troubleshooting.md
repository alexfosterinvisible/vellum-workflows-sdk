🚨 IMPORTANT: This is a living document of key learnings from working with the Vellum SDK. Each instruction is based on practical experience and should be updated as we learn more.

# Troubleshooting Guide

## Quick Checks

```bash
# Check all common issues in one go
vellum-explorer check-auth && vellum-explorer list && vellum-explorer execute test-prompt --inputs '{"test": "value"}' || echo "Found issues, see below"

# Verify environment setup
python -c "from vellum.client import Vellum; import os; print('API Key Set' if os.getenv('VELLUM_API_KEY') else 'Missing API Key')" && pip freeze | grep -E "vellum|rich"

# Test rate limits and response parsing
for i in {1..5}; do vellum-explorer execute test-prompt --inputs '{"test": "batch-$i"}' --delay 1; done
```

## Common Issues and Solutions

### 1. Authentication Errors

**Problem**: `Invalid API key or unauthorized access` | **Quick Fix**: `echo "VELLUM_API_KEY=your_key" > .env && source .env`

- Check `.env` file exists and contains valid API key | Verify API key permissions | Ensure environment variables are loaded

### 2. Prompt Execution Failures

**Problem**: `Prompt execution returns REJECTED state` | **Quick Fix**: `vellum-explorer validate <prompt-name>`

```python
# Add to your code for robust execution
def safe_execute(prompt_name, inputs, max_retries=3):
    for i in range(max_retries):
        try: return client.execute_prompt(prompt_name, inputs=inputs)
        except Exception as e: time.sleep(2 ** i)
    return None
```

### 3. Rate Limiting & Input Validation

```python
# Combined solution for rate limits and input validation
def execute_with_validation(prompt_name, inputs, max_retries=3):
    if not isinstance(inputs, dict) or not all(isinstance(k, str) and isinstance(v, str) for k,v in inputs.items()): 
        raise ValueError("Invalid inputs")
    return safe_execute(prompt_name, inputs, max_retries)
```

### 4. Response Parsing & Error Handling

```python
# One-liner for safe response handling
safe_get_output = lambda r: None if not r or not hasattr(r, 'outputs') else [o.value for o in r.outputs if hasattr(o, 'value')]
```

## Debug Checklist & Quick Fixes

```bash
# Run all checks in sequence
bash -c '
echo "1. Environment Check" && \
python -c "import vellum" && \
echo "2. API Key Check" && \
vellum-explorer list && \
echo "3. Prompt Execution" && \
vellum-explorer execute test-prompt --inputs "{\"test\": \"value\"}" && \
echo "4. Rate Limit Test" && \
for i in {1..3}; do vellum-explorer list; sleep 1; done && \
echo "All checks passed!"
'
```

## PI API Troubleshooting

### Quick Checks

```bash
# Test API connection and auth
curl -I -H "x-api-key: $PI_API_KEY" https://api.withpi.ai/v1/contracts/generate_dimensions

# Verify contract generation
python -c "
import asyncio, aiohttp
async def test():
    async with aiohttp.ClientSession(headers={'x-api-key': '$PI_API_KEY'}) as s:
        async with s.post('https://api.withpi.ai/v1/contracts/generate_dimensions', 
            json={'contract': {'name': 'Test', 'description': 'Test contract'}}) as r:
            print(f'Status: {r.status}')
asyncio.run(test())
"
```

### Common Issues and Solutions

1. **Authentication Errors**
   **Problem**: `{"detail":"Not authenticated"}`
   **Quick Fix**: Check header is `x-api-key` not `Authorization`

   ```python
   # Correct
   headers = {"x-api-key": API_KEY}
   # Wrong
   headers = {"Authorization": f"Bearer {API_KEY}"}
   ```

2. **Contract Generation Failures**
   **Problem**: `500 Internal Server Error` on scoring
   **Quick Fix**: Ensure you're using the generated dimensions

   ```python
   # Always generate dimensions first
   contract_with_dims = await generate_dimensions(contract)
   # Then use for scoring
   await score_contract(contract_with_dims, input_text, output_text)
   ```

3. **Scoring Issues**
   **Problem**: Unexpected low scores
   **Quick Fix**: Add detailed explanations in outputs

   ```python
   # Bad
   output = "The answer is 4."
   
   # Good
   output = """The answer is 4. Let me explain:
   1. We start with 2 + 2
   2. Adding these numbers
   3. Results in 4
   Therefore, 2 + 2 = 4."""
   ```

### Debug Checklist

1. **API Connection**

   ```python
   async def check_api():
       async with session.get(BASE_URL) as resp:
           print(f"Status: {resp.status}")
           print(f"Headers: {dict(resp.headers)}")
   ```

2. **Contract Generation**

   ```python
   async def debug_contract(contract):
       # Test contract structure
       print(f"Contract: {json.dumps(contract, indent=2)}")
       
       # Generate dimensions
       dims = await generate_dimensions(contract)
       print(f"Dimensions: {json.dumps(dims, indent=2)}")
       
       return dims
   ```

3. **Score Analysis**

   ```python
   async def analyze_scores(scores):
       print(f"Total Score: {scores['total_score']}")
       for dim, data in scores['dimension_scores'].items():
           print(f"\n{dim}:")
           print(f"  Total: {data['total_score']}")
           for sub, score in data['subdimension_scores'].items():
               print(f"  - {sub}: {score}")
   ```

## Development Workflow

I have checked, and I maintained your comments and docstrings.
