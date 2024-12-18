# Folders API

## Overview
The Folders API allows you to organize and manage entities (prompts, workflows, documents, etc.) in a hierarchical structure.

## Endpoints

### Add Entity to Folder (Beta)
```http
POST https://api.vellum.ai/v1/folders/:folder_id/add-entity
```

Add an entity to a specific folder or root directory.

#### Request
```json
{
  "entity_id": "entity_123"
}
```

#### Root Directories
- `PROMPT_SANDBOX`
- `WORKFLOW_SANDBOX`
- `DOCUMENT_INDEX`
- `TEST_SUITE`

### List Folder Entities (Beta)
```http
GET https://api.vellum.ai/v1/folder-entities
```

List all entities within a specified folder.

#### Parameters
- `parent_folder_id`: ID of parent folder or root directory
- `entity_status`: Filter by status ("ACTIVE" or "ARCHIVED")
- `limit`: Results per page
- `offset`: Pagination offset
- `ordering`: Sort field

#### Response
```json
{
  "count": 25,
  "results": [
    {
      "type": "PROMPT_SANDBOX",
      "id": "entity_123",
      "data": {
        "id": "sandbox_123",
        "label": "Customer Support Prompts",
        "created": "2024-01-15T09:30:00Z",
        "modified": "2024-01-15T09:30:00Z",
        "status": "ACTIVE"
      }
    }
  ]
}
```

## Client Examples

### Python
```python
from vellum import Client

client = Client(api_key="your-api-key")

# Add entity to folder
client.add_entity_to_folder(
    folder_id="folder_123",
    entity_id="entity_123"
)

# List folder contents
entities = client.list_folder_entities(
    parent_folder_id="folder_123",
    entity_status="ACTIVE",
    limit=10
)

# List root directory
root_entities = client.list_folder_entities(
    parent_folder_id="PROMPT_SANDBOX",
    limit=10
)
```

### TypeScript
```typescript
import { Client } from '@vellum-ai/client';

const client = new Client({ apiKey: 'your-api-key' });

// Add entity to folder
await client.addEntityToFolder({
  folderId: 'folder_123',
  entityId: 'entity_123'
});

// List folder contents
const entities = await client.listFolderEntities({
  parentFolderId: 'folder_123',
  entityStatus: 'ACTIVE',
  limit: 10
});

// List root directory
const rootEntities = await client.listFolderEntities({
  parentFolderId: 'PROMPT_SANDBOX',
  limit: 10
});
```

## Best Practices

### Folder Organization
1. Logical Grouping
   - Group related entities
   - Use consistent naming
   - Maintain clear hierarchy
   - Document organization

2. Access Management
   - Control folder access
   - Monitor usage patterns
   - Audit folder changes
   - Regular cleanup

3. Entity Management
   - Track entity locations
   - Handle moves carefully
   - Maintain references
   - Update dependencies

### Performance
1. Folder Operations
   - Batch entity moves
   - Optimize listings
   - Cache folder structure
   - Monitor large folders

2. Error Handling
```python
try:
    client.add_entity_to_folder(...)
except VellumError as e:
    if e.code == "ENTITY_NOT_FOUND":
        # Handle missing entity
    elif e.code == "FOLDER_NOT_FOUND":
        # Handle missing folder
    elif e.code == "INVALID_OPERATION":
        # Handle invalid move
```

## Root Directory Types

### PROMPT_SANDBOX
- Stores prompt templates
- Manages prompt versions
- Organizes prompt tests
- Groups related prompts

### WORKFLOW_SANDBOX
- Contains workflow definitions
- Manages workflow versions
- Organizes workflow tests
- Groups related workflows

### DOCUMENT_INDEX
- Stores document indexes
- Manages document collections
- Organizes search configurations
- Groups related documents

### TEST_SUITE
- Contains test suites
- Manages test cases
- Organizes test runs
- Groups related tests

## Rate Limits
- Entity operations: 10 requests/second
- List operations: 20 requests/second
- Enterprise: Custom limits

## Support
- [API Reference](https://docs.vellum.ai/api/folders)
- [Examples](https://github.com/vellum-ai/examples)
- [Support](https://support.vellum.ai) 