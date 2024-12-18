# Documents API

## Overview
The Documents API enables you to upload, manage, and retrieve documents that can be used for search and retrieval.

## Endpoints

### Upload Document (GA)
```http
POST https://documents.vellum.ai/v1/upload-document
```

Upload a document to be indexed and used for search. Uses multipart/form-data.

#### Request
```bash
curl -X POST https://documents.vellum.ai/v1/upload-document \
  -H "X_API_KEY: your-api-key" \
  -F "contents=@document.pdf" \
  -F 'metadata={"source": "manual", "category": "guide"}' \
  -F "label=User Guide" \
  -F "add_to_index_names=[\"my-index\"]"
```

#### Response
```json
{
  "document_id": "doc_123",
  "status": "PROCESSING"
}
```

### List Documents (GA)
```http
GET https://api.vellum.ai/v1/documents
```

Retrieve a list of documents, optionally filtered by index.

#### Parameters
- `document_index_id`: Filter by index
- `limit`: Results per page
- `offset`: Pagination offset
- `ordering`: Sort field

#### Response
```json
{
  "count": 100,
  "results": [
    {
      "id": "doc_123",
      "label": "User Guide",
      "last_uploaded_at": "2024-01-15T09:30:00Z",
      "processing_state": "PROCESSED",
      "metadata": {
        "source": "manual",
        "category": "guide"
      }
    }
  ]
}
```

### Retrieve Document (Beta)
```http
GET https://api.vellum.ai/v1/documents/:id
```

Get details about a specific document.

#### Response
```json
{
  "id": "doc_123",
  "label": "User Guide",
  "last_uploaded_at": "2024-01-15T09:30:00Z",
  "processing_state": "PROCESSED",
  "metadata": {
    "source": "manual",
    "category": "guide"
  },
  "document_to_document_indexes": [
    {
      "document_index_id": "index_123"
    }
  ]
}
```

## Client Examples

### Python
```python
from vellum import Client

client = Client(api_key="your-api-key")

# Upload document
with open("document.pdf", "rb") as f:
    doc = client.upload_document(
        contents=f,
        label="User Guide",
        metadata={"source": "manual"},
        add_to_index_names=["my-index"]
    )

# List documents
docs = client.list_documents(
    document_index_id="index_123",
    limit=10
)

# Get document details
doc = client.get_document(id="doc_123")

# Update document metadata
doc = client.update_document(
    id="doc_123",
    metadata={"category": "updated"}
)
```

### TypeScript
```typescript
import { Client } from '@vellum-ai/client';

const client = new Client({ apiKey: 'your-api-key' });

// Upload document
const formData = new FormData();
formData.append('contents', file);
formData.append('label', 'User Guide');
formData.append('metadata', JSON.stringify({ source: 'manual' }));
formData.append('add_to_index_names', JSON.stringify(['my-index']));

const doc = await client.uploadDocument(formData);

// List documents
const docs = await client.listDocuments({
  documentIndexId: 'index_123',
  limit: 10
});

// Get document details
const doc = await client.getDocument('doc_123');

// Update document metadata
const updatedDoc = await client.updateDocument({
  id: 'doc_123',
  metadata: { category: 'updated' }
});
```

## Best Practices

### Document Upload
1. Use appropriate file formats
   - PDF
   - Text
   - Word documents
   - Markdown
   - HTML

2. Metadata Management
   - Include relevant metadata
   - Use consistent schemas
   - Keep metadata concise
   - Update when needed

3. Processing States
   - Monitor upload status
   - Handle processing errors
   - Retry failed uploads
   - Check final state

4. File Size Limits
   - Maximum: 100MB per file
   - Split large documents
   - Consider chunking
   - Optimize file size

### Performance
1. Batch Operations
   - Group related uploads
   - Use bulk updates
   - Implement rate limiting
   - Monitor quotas

2. Error Handling
```python
try:
    doc = client.upload_document(...)
except VellumError as e:
    if e.code == "FILE_TOO_LARGE":
        # Handle large files
    elif e.code == "INVALID_FORMAT":
        # Handle format issues
    elif e.code == "PROCESSING_ERROR":
        # Handle processing errors
```

## Rate Limits
- Upload: 5 requests/second
- List/Retrieve: 20 requests/second
- Update: 10 requests/second
- Enterprise: Custom limits

## Support
- [API Reference](https://docs.vellum.ai/api/documents)
- [Examples](https://github.com/vellum-ai/examples)
- [Support](https://support.vellum.ai) 