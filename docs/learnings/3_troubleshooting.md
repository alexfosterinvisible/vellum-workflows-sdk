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

I have checked, and I maintained your comments and docstrings.