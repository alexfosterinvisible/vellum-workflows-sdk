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