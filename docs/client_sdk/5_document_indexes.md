# Document Indexes API

## Overview
The Document Indexes API allows you to create, manage, and search document indexes for semantic search and retrieval.

## Endpoints

### Search (GA)
```http
POST https://predict.vellum.ai/v1/search
```

Perform a semantic search against a document index.

#### Request
```json
{
  "query": "search query string",
  "index_id": "string",
  "index_name": "string",
  "options": {
    "limit": 10,
    "min_score": 0.7,
    "filters": {}
  }
}
```

#### Response
```json
{
  "results": [
    {
      "id": "chunk_id",
      "content": "Matching content",
      "score": 0.95,
      "metadata": {},
      "document_id": "source_doc_id"
    }
  ]
}
```

### Create Document Index (Beta)
```http
POST https://api.vellum.ai/v1/document-indexes
```

Creates a new document index.

#### Request
```json
{
  "label": "My Document Index",
  "name": "my-document-index",
  "indexing_config": {
    "vectorizer": {
      "model_name": "text-multilingual-embedding-002",
      "config": {
        "project_id": "project_id",
        "region": "region"
      }
    },
    "chunking": {
      "chunker_name": "token-overlapping-window-chunker"
    }
  },
  "status": "ACTIVE",
  "environment": "PRODUCTION"
}
```

### Add Document to Index (Beta)
```http
POST https://api.vellum.ai/v1/document-indexes/:id/documents/:document_id
```

Adds a previously uploaded document to an index.

## Client Examples

### Python
```python
from vellum import Client

client = Client(api_key="your-api-key")

# Search documents
results = client.search(
    index_name="my-index",
    query="How do I get started?",
    options={
        "limit": 5,
        "min_score": 0.7
    }
)

# Create index
index = client.create_document_index(
    name="my-index",
    label="My Index",
    indexing_config={
        "vectorizer": {
            "model_name": "text-multilingual-embedding-002"
        },
        "chunking": {
            "chunker_name": "token-overlapping-window-chunker"
        }
    }
)

# Add document to index
client.add_document_to_index(
    index_id=index.id,
    document_id="doc_id"
)
```

### TypeScript
```typescript
import { Client } from '@vellum-ai/client';

const client = new Client({ apiKey: 'your-api-key' });

// Search documents
const results = await client.search({
  indexName: 'my-index',
  query: 'How do I get started?',
  options: {
    limit: 5,
    minScore: 0.7
  }
});

// Create index
const index = await client.createDocumentIndex({
  name: 'my-index',
  label: 'My Index',
  indexingConfig: {
    vectorizer: {
      modelName: 'text-multilingual-embedding-002'
    },
    chunking: {
      chunkerName: 'token-overlapping-window-chunker'
    }
  }
});

// Add document to index
await client.addDocumentToIndex({
  indexId: index.id,
  documentId: 'doc_id'
});
```

## Best Practices

### Search
1. Use specific queries
2. Set appropriate score thresholds
3. Implement pagination
4. Cache frequent queries

### Indexing
1. Choose appropriate chunking
2. Select suitable embedding model
3. Use metadata for filtering
4. Monitor index size

### Performance
1. Batch document additions
2. Use filters to narrow search
3. Cache search results
4. Monitor query latency

## Rate Limits
- Search: 20 requests/second
- Index operations: 5 requests/second
- Document additions: 10 requests/second
- Enterprise: Custom limits

## Support
- [API Reference](https://docs.vellum.ai/api/document-indexes)
- [Examples](https://github.com/vellum-ai/examples)
- [Support](https://support.vellum.ai) 