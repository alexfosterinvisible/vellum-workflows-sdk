# Vellum CLI

The Vellum CLI is a command-line interface for interacting with Vellum. It enables you to synchronize resources between the Vellum application and the Vellum SDKs.

## Commands

### Pull Command

```bash
vellum workflows pull [module] [options]
```

Used to pull Vellum resources from the Vellum application into your local SDK.

#### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `module` | str | No | The module to pull the workflow into. If not provided, a module will be generated based on the Workflow Sandbox ID. |

#### Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--workflow-sandbox-id` | str | No* | Pull the Workflow from a specific Sandbox ID. Required if `module` is not provided. If not provided, uses the Workflow Sandbox ID from `pyproject.toml` associated with the module. |
| `--include-json` | bool | No | Include the JSON representation of the Workflow in the pull response. For debugging only. |
| `--exclude-code` | bool | No | Exclude the code definition of the Workflow from the pull response. For debugging only. |

#### Example Usage

```bash
# Pull using module name
vellum workflows pull my.example

# Pull using sandbox ID
vellum workflows pull --workflow-sandbox-id abc123

# Pull with debugging options
vellum workflows pull my.example --include-json
```

### Push Command

```bash
vellum workflows push [module] [options]
```

Used to push Vellum resources defined with the SDK to the Vellum application.

#### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `module` | str | No | The module to push from local. If not provided, uses the first module defined in `pyproject.toml`. |

#### Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--deploy` | bool | No | Automatically deploy the Workflow after pushing to Vellum. |
| `--deployment-label` | str | No* | Label for the deployment. Requires `--deploy`. |
| `--deployment-name` | str | No* | Name for the deployment. Requires `--deploy`. |
| `--deployment-description` | str | No* | Description for the deployment. Requires `--deploy`. |
| `--release-tag` | List[str] | No* | Release tags for the deployment. Requires `--deploy`. |

#### Example Usage

```bash
# Basic push
vellum workflows push my.example

# Push and deploy with options
vellum workflows push my.example \
    --deploy \
    --deployment-label "Production v1.0" \
    --deployment-name "prod-v1" \
    --deployment-description "Initial production release" \
    --release-tag "v1.0.0" "production"
```

### Basic Commands

- `list` - List available prompts and their status
- `execute` - Execute a prompt with inputs
- `validate` - Validate prompt configuration
- `ask` - Ask natural language questions about documentation

### Command Details

#### ask

Ask natural language questions about Vellum documentation and get AI-powered responses.

```bash
vellum-explorer ask "your question here"
```

Features:
- Natural language understanding
- Parallel documentation search
- Code examples when relevant
- Confidence scoring
- Supporting evidence with sources

Example:
```bash
# Ask about authentication
vellum-explorer ask "How do I handle API keys?"

# Ask about error handling
vellum-explorer ask "What's the proper way to handle errors?"

# Ask about features
vellum-explorer ask "What export formats are supported?"
```

The response includes:
1. Direct answer to your question
2. Supporting quotes from documentation
3. Relevant code examples
4. Confidence scores for the response

## Configuration

The CLI uses configuration from your `pyproject.toml` file. Example configuration:

```toml
[tool.vellum.workflows]
modules = [
    "my.example"
]

[tool.vellum.workflows.my.example]
sandbox_id = "abc123"
```

## Best Practices

1. **Version Control**
   - Always pull before making local changes
   - Push changes to version control before deploying

2. **Deployment**
   - Use meaningful deployment labels and tags
   - Include descriptive deployment descriptions
   - Follow a consistent release tag strategy

3. **Development Flow**

   ```bash
   # Start development
   vellum workflows pull my.example
   
   # After making changes
   vellum workflows push my.example
   
   # When ready for production
   vellum workflows push my.example --deploy --release-tag "production"
   ```

## Related Topics

- [Workflows SDK Introduction](/developers/workflows-sdk/introduction)
- [Configuration Guide](/developers/workflows-sdk/configuration)
- [Deployment Best Practices](/developers/workflows-sdk/deployment)
