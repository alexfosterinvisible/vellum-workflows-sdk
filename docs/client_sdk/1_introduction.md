# Vellum Client SDK & API Reference

Welcome to Vellum's Client SDK and API documentation! Here you'll find comprehensive information about our HTTP endpoints, request/response formats, and client libraries.

## Overview

### Base URLs
- Default: `https://api.vellum.ai`
- Document Upload: `https://documents.vellum.ai`
- Prediction/Execution: `https://predict.vellum.ai`

### API Stability
- **GA (Generally Available)**: Stable APIs ready for production use
- **Beta**: APIs under active development that may change

### Official API Clients
Vellum maintains official API clients for:
- [Python](https://github.com/vellum-ai/vellum-client-python)
- [Node/TypeScript](https://github.com/vellum-ai/vellum-client-node)
- [Go](https://github.com/vellum-ai/vellum-client-go)

## Response Formats

### Standard Fields
- `id`: Unique identifier
- `created`: Creation timestamp
- `modified`: Last modification timestamp
- `status`: Current status (e.g., "ACTIVE", "ARCHIVED")
- `label`: Human-readable label
- `name`: Unique name within workspace

### Status Codes
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `429`: Rate Limited
- `500`: Server Error

### Pagination
Many list endpoints support pagination with:
- `limit`: Results per page
- `offset`: Starting index
- `ordering`: Sort field

## Best Practices

### Error Handling
1. Check response status codes
2. Implement retries with backoff
3. Handle rate limits
4. Log errors properly

### Security
1. Rotate API keys regularly
2. Use environment variables
3. Implement access controls
4. Monitor API usage

### Development
1. Use Beta APIs in development
2. Use GA APIs in production
3. Follow versioning guidelines
4. Implement proper error handling

## Support
- [Documentation](https://docs.vellum.ai)
- [API Status](https://status.vellum.ai)
- [Support Portal](https://support.vellum.ai) 