# Secrets API

## Overview
The Secrets API enables you to manage sensitive information like API keys, credentials, and other configuration values securely.

## Endpoints

### Retrieve Workspace Secret (Beta)
```http
GET https://api.vellum.ai/v1/workspace-secrets/:id
```

Retrieve a workspace secret by ID or name.

#### Response
```json
{
  "id": "secret_123",
  "modified": "2024-01-15T09:30:00Z",
  "name": "API_KEY",
  "label": "External API Key",
  "secret_type": "USER_DEFINED"
}
```

### Update Workspace Secret (Beta)
```http
PATCH https://api.vellum.ai/v1/workspace-secrets/:id
```

Update an existing workspace secret.

#### Request
```json
{
  "label": "Updated API Key",
  "value": "new-secret-value"
}
```

## Secret Types

### USER_DEFINED
- Custom secrets defined by users
- API keys for external services
- Configuration values
- Credentials

### HMAC
- Cryptographic keys
- Signing secrets
- Verification tokens
- Security credentials

### INTERNAL_API_KEY
- Vellum-specific API keys
- Internal service credentials
- System-level secrets
- Integration tokens

## Client Examples

### Python
```python
from vellum import Client

client = Client(api_key="your-api-key")

# Get secret
secret = client.get_workspace_secret(
    id="secret_123"
)

# Update secret
updated_secret = client.update_workspace_secret(
    id="secret_123",
    label="Updated API Key",
    value="new-secret-value"
)
```

### TypeScript
```typescript
import { Client } from '@vellum-ai/client';

const client = new Client({ apiKey: 'your-api-key' });

// Get secret
const secret = await client.getWorkspaceSecret('secret_123');

// Update secret
const updatedSecret = await client.updateWorkspaceSecret({
  id: 'secret_123',
  label: 'Updated API Key',
  value: 'new-secret-value'
});
```

## Best Practices

### Security
1. Access Control
   - Limit secret access
   - Audit secret usage
   - Regular rotation
   - Secure transmission

2. Secret Management
   - Use descriptive labels
   - Document purpose
   - Track modifications
   - Version control

3. Value Guidelines
   - Use strong values
   - Avoid patterns
   - Limit sharing
   - Secure storage

### Error Handling
```python
try:
    secret = client.get_workspace_secret(...)
except VellumError as e:
    if e.code == "SECRET_NOT_FOUND":
        # Handle missing secret
    elif e.code == "INVALID_SECRET_TYPE":
        # Handle type mismatch
    elif e.code == "ACCESS_DENIED":
        # Handle permissions
```

## Secret Usage

### In Workflows
```python
class MyWorkflow(BaseWorkflow):
    def run(self):
        # Access secret in workflow
        api_key = self.get_secret("API_KEY")
        # Use api_key securely
```

### In Prompts
```python
class MyPrompt(BasePrompt):
    def execute(self):
        # Access secret in prompt
        credentials = self.get_secret("SERVICE_CREDS")
        # Use credentials securely
```

### In Tests
```python
class MyTest(BaseTest):
    def setup(self):
        # Access secret in test
        test_key = self.get_secret("TEST_API_KEY")
        # Use test_key for testing
```

## Security Guidelines

### Storage
- Encrypted at rest
- Secure transmission
- Access logging
- Regular backups

### Rotation
1. Schedule
   - Development: Monthly
   - Production: Quarterly
   - Critical: Monthly
   - Custom: As needed

2. Process
   - Create new secret
   - Update references
   - Verify functionality
   - Remove old secret

### Monitoring
1. Access Patterns
   - Track usage
   - Monitor failures
   - Alert on anomalies
   - Log rotations

2. Security Events
   - Failed attempts
   - Unauthorized access
   - Modification alerts
   - Rotation reminders

## Rate Limits
- Retrieval: 20 requests/second
- Updates: 5 requests/second
- Enterprise: Custom limits

## Support
- [API Reference](https://docs.vellum.ai/api/secrets)
- [Examples](https://github.com/vellum-ai/examples)
- [Support](https://support.vellum.ai) 