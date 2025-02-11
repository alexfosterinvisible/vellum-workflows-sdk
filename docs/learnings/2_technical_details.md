🚨 IMPORTANT: This is a living document of key learnings from working with the Vellum SDK. Each instruction is based on practical experience and should be updated as we learn more.

# Technical Implementation Details

## API Integration

### Client Setup

```python
from vellum.client import Vellum
client = Vellum(api_key=api_key)
```

### Key Components

1. **PromptInfo Dataclass**

   ```python
   @dataclass
   class PromptInfo:
       id: str
       name: str
       label: str
       created: datetime
       last_deployed: datetime
       status: str
       environment: str
       description: Optional[str] = None
   ```

2. **Input Handling**

   ```python
   vellum_inputs = [
       types.PromptRequestStringInput(
           name=name,
           key="",
           value=value
       )
       for name, value in inputs.items()
   ]
   ```

3. **Error Handling Pattern**

   ```python
   try:
       result = client.execute_prompt(
           prompt_deployment_name=name,
           release_tag=tag,
           inputs=inputs
       )
       if result.state == "REJECTED":
           handle_rejection(result.error)
   except Exception as e:
       handle_exception(e)
   ```

4. **Deployment Retrieval Pattern**

   ```python
   # No direct get method exists, use list and filter
   response = client.deployments.list()
   deployment = next(
       (d for d in response.results if d.name == prompt_name),
       None
   )
   ```

## CLI Implementation

### Command Structure

```python
@click.group()
@click.option('--api-key', envvar='VELLUM_API_KEY')
@click.pass_context
def cli(ctx, api_key):
    ctx.ensure_object(dict)
    ctx.obj['explorer'] = PromptExplorer(api_key=api_key)
```

### Rich Console Usage

```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Prompts")
console.print(table)
```

### Streaming Output

```bash
# Basic streaming execution
vellum-explorer execute my-prompt --inputs '{"var": "value"}' --stream

# Note: Streaming mode disables Rich formatting for real-time output
# Use regular mode for formatted output:
vellum-explorer execute my-prompt --inputs '{"var": "value"}'
```

### Export Functionality

```bash
# Export to CSV (all prompts)
vellum-explorer list --export prompts.csv

# Export execution results
vellum-explorer execute my-prompt --inputs '{"var": "value"}' --export results.xlsx

# Supported formats: csv, xlsx, json
```

## Testing Considerations

1. **Mock API Responses**

   ```python
   @pytest.fixture
   def mock_vellum_client(mocker):
       return mocker.patch('vellum.client.Vellum')
   ```

2. **Input Validation**

   ```python
   def validate_inputs(inputs: Dict[str, str]) -> bool:
       return all(
           isinstance(k, str) and isinstance(v, str)
           for k, v in inputs.items()
       )
   ```

## Performance Optimizations

1. **Caching Strategy**
   - Cache prompt list results
   - Implement TTL for cached items
   - Clear cache on version changes

2. **Rate Limiting**
   - Implement exponential backoff
   - Track API usage
   - Queue requests when near limits

## Development Workflow

1. **Git Operations**

   ```bash
   # Always execute git commands from project root
   cd /path/to/project && git add prompts_CLI/ && git commit -m "feat: Add feature"
   
   # Create feature branch
   git checkout -b feat/feature-name
   
   # Check branch status
   git status
   ```

2. **Common Issues & Solutions**
   - Vellum client lacks direct `get` method for deployments -> Use `list()` and filter
   - Git commands failing -> Always execute from project root
   - Missing imports -> Check package versions in requirements.txt
   - API errors -> Check environment variables and permissions

3. **Best Practices**

   ```bash
   # Run all checks in sequence
   cd /project/root && \
   python -m pytest && \
   flake8 prompts_CLI/ && \
   git status && \
   git add . && \
   git commit -m "type: description"
   ```

## PI API Contract Testing

### Client Setup

```python
import aiohttp

async with aiohttp.ClientSession(headers={
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}) as session:
    # API calls here
```

### Contract Generation

```python
async def generate_dimensions(contract: Dict) -> Dict:
    """Generate dimensions for a contract."""
    async with session.post(
        "https://api.withpi.ai/v1/contracts/generate_dimensions",
        json={"contract": contract}
    ) as resp:
        if resp.status == 200:
            return await resp.json()
        raise Exception(f"Failed to generate dimensions: {await resp.text()}")
```

### Contract Scoring

```python
async def score_contract(
    contract: Dict,
    llm_input: str,
    llm_output: str
) -> Dict[str, float]:
    """Score an input/output pair against a contract."""
    async with session.post(
        "https://api.withpi.ai/v1/contracts/score",
        json={
            "contract": contract,
            "llm_input": llm_input,
            "llm_output": llm_output
        }
    ) as resp:
        if resp.status == 200:
            data = await resp.json()
            return {
                "total_score": data["total_score"],
                "dimension_scores": data["dimension_scores"]
            }
        raise Exception(f"Failed to score contract: {await resp.text()}")
```

### Response Structure

```python
# Contract Generation Response
{
    "name": str,
    "description": str,
    "dimensions": [
        {
            "label": str,
            "description": str,
            "weight": float,
            "sub_dimensions": [
                {
                    "label": str,
                    "description": str,
                    "scoring_type": "PI_SCORER",
                    "parameters": [float],  # 5 values for Likert scale
                    "weight": float
                }
            ]
        }
    ]
}

# Contract Scoring Response
{
    "total_score": float,  # 0.0 to 1.0
    "dimension_scores": {
        "dimension_name": {
            "total_score": float,
            "subdimension_scores": {
                "subdimension_name": float
            }
        }
    }
}
```

### Error Handling Pattern

```python
async def safe_api_call(func, *args, **kwargs):
    """Execute API call with retries and error handling."""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientError as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(retry_delay * (attempt + 1))
        except Exception as e:
            if "rate limit" in str(e).lower():
                await asyncio.sleep(60)  # Rate limit cooldown
                continue
            raise
```

### Testing Considerations

1. **Contract Generation**
   - Test with various contract descriptions
   - Verify dimension generation consistency
   - Check subdimension parameter ranges

2. **Contract Scoring**
   - Test with known good/bad examples
   - Verify score distributions
   - Monitor dimension weight impacts

3. **Error Cases**
   - Test rate limit handling
   - Verify authentication errors
   - Check malformed input handling

## Development Workflow

# ... rest of existing code
