# Authentication

## Generating API Keys
The Vellum API uses API keys to authenticate requests. You can view and manage your API keys in the [Vellum Dashboard](https://app.vellum.ai/api-keys).

## Using API Keys

### Headers
Include your API key in the `X_API_KEY` header in your requests:

```bash
curl -H "X_API_KEY: your-api-key" https://api.vellum.ai/v1/endpoint
```

### Client Libraries
When using official client libraries:

```python
# Python
from vellum import Client
client = Client(api_key="your-api-key")
```

```typescript
// TypeScript
import { Client } from '@vellum-ai/client';
const client = new Client({ apiKey: 'your-api-key' });
```

```go
// Go
import "github.com/vellum-ai/vellum-client-go"
client := vellum.NewClient("your-api-key")
```

## Security Requirements

1. **HTTPS Required**
   - All API requests must use HTTPS
   - Plain HTTP requests will fail
   - API requests without authentication will fail

2. **API Key Best Practices**
   - Treat API keys like passwords
   - Never share keys in public repositories
   - Don't include keys in client-side code
   - Use environment variables or secure secret management
   - Rotate keys regularly
   - Use different keys for development and production

## Environment-Specific Keys

We recommend using different API keys for different environments:

- Development: Limited rate limits, more lenient error handling
- Staging: Production-like settings for testing
- Production: Higher rate limits, stricter security

## Rate Limiting

API keys are subject to rate limiting:

- Limits vary by endpoint and plan
- Rate limit headers are included in responses
- Implement exponential backoff for retries
- Monitor usage to avoid hitting limits

## Key Management

### Storage
```bash
# Environment variables (recommended)
export VELLUM_API_KEY=your-api-key

# .env file (development only)
VELLUM_API_KEY=your-api-key
```

### Rotation Schedule
- Development: Monthly
- Production: Quarterly
- Immediate rotation if compromised

### Access Control
- Limit key access to necessary team members
- Use separate keys for different services
- Document key usage and ownership
- Implement key rotation procedures

## Troubleshooting

### Common Issues
1. Invalid API key
2. Expired API key
3. Rate limit exceeded
4. Wrong environment key

### Error Responses
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid API key provided"
  }
}
```

## Support
If you encounter authentication issues:
1. Verify key validity in dashboard
2. Check environment configuration
3. Review security logs
4. Contact [Vellum Support](https://support.vellum.ai) if needed 