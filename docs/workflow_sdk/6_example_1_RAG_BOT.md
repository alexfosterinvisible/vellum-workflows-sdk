# Examples

## Basic RAG Chatbot

### Overview

This example demonstrates how to build a basic RAG (Retrieval-Augmented Generation) chatbot that answers questions using content from PDF documents. The example uses Vellum's Trust Center Policies as the knowledge base, making it useful for scaling support teams by providing accurate answers to common customer questions.

### Workflow Steps

1. `ExtractUserMessage`: Extracts the most recent message from the chat history
2. `SearchNode`: Performs semantic search to find relevant quotes from ingested PDFs
3. `FormatSearchResultsNode`: Formats search results with source document metadata
4. `PromptNode`: Generates a response using the context and user's question

### Graph Definition

```python
class BasicRAGWorkflow(BaseWorkflow[Inputs, BaseState]):
    """RAG chatbot workflow for answering policy questions"""
    graph = ExtractUserMessage >> SearchNode >> FormatSearchResultsNode >> PromptNode
    
    class Outputs(BaseWorkflow.Outputs):
        result = PromptNode.Outputs.text
```

### Project Setup

1. Install dependencies:
```bash
pip install vellum-ai
```

2. Create project structure:
```
basic_rag_chatbot/
├── workflow.py          # Main workflow definition
├── inputs.py           # Input type definitions
├── __init__.py
└── nodes/              # Individual node implementations
    ├── __init__.py
    ├── extract_user_message.py
    ├── search_node.py
    ├── format_search_results_node.py
    └── prompt_node.py
```

> **Note**: This folder structure is required for UI-code synchronization. If not using the UI, any structure is fine.

### Implementation

#### 1. Define Workflow Inputs (`inputs.py`)

```python
from typing import List
from vellum.workflows.inputs import BaseInputs
from vellum import ChatMessageRequest

class Inputs(BaseInputs):
    """Input schema for the RAG chatbot workflow"""
    chat_history: List[ChatMessageRequest]
```

#### 2. Implement Nodes

##### Extract User Message (`nodes/extract_user_message.py`)
```python
from vellum.workflows.nodes import TemplatingNode

class ExtractUserMessage(TemplatingNode):
    """Extracts the latest user message from chat history"""
    template = "{{ chat_history[-1]['text'] }}"
    inputs = {
        "chat_history": Inputs.chat_history,
    }
```

##### Search Node (`nodes/search_node.py`)
```python
from vellum.workflows.nodes import BaseSearchNode

class SearchNode(BaseSearchNode):
    """Performs semantic search against document index"""
    document_index = "vellum-trust-center-policies"
    query = ExtractUserMessage.Outputs.result
```

##### Format Search Results (`nodes/format_search_results_node.py`)
```python
from vellum.workflows.nodes import TemplatingNode

class FormatSearchResultsNode(TemplatingNode):
    """Formats search results with document sources"""
    template = """\
        {% for result in results -%}
        Policy: {{ result.document.label }}
        ------
        {{ result.text }}
        {% if not loop.last %}
        #####
        {% endif -%}
        {% endfor %}\
    """
    inputs = {
        "results": SearchNode.Outputs.results,
    }
```

##### Prompt Node (`nodes/prompt_node.py`)
```python
from vellum.workflows.nodes import InlinePromptNode
from vellum import (
    ChatMessagePromptBlock,
    ChatMessageRequest,
    JinjaPromptBlock,
)

class PromptNode(InlinePromptNode):
    """Generates response using context and question"""
    ml_model = "gpt-4o"
    prompt_inputs = {
        "question": ExtractUserMessage.Outputs.result,
        "context": FormatSearchResultsNode.Outputs.result,
    }
    blocks = [
        ChatMessagePromptBlock(
            chat_role="SYSTEM",
            blocks=[
                JinjaPromptBlock(
                    template="""\
                        Answer user question based on the context provided below. 
                        If you don't know the answer say "Sorry I don't know"

                        **Context**
                        ```
                        {{ context }}
                        ```

                        Guidelines:
                        - Limit answer to 250 words
                        - Provide citation at the end
                        - Use direct quotes when possible
                        - Maintain professional tone\
                    """,
                ),
            ],
        ),
        ChatMessagePromptBlock(
            chat_role="USER", 
            blocks=[
                JinjaPromptBlock(
                    template="{{ question }}"
                ),
            ],
        ),
    ]
```

#### 3. Define Workflow (`workflow.py`)

```python
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState
from .nodes import (
    ExtractUserMessage,
    SearchNode,
    FormatSearchResultsNode,
    PromptNode,
)

class BasicRAGWorkflow(BaseWorkflow[Inputs, BaseState]):
    """RAG chatbot workflow for answering policy questions"""
    graph = ExtractUserMessage >> SearchNode >> FormatSearchResultsNode >> PromptNode
    
    class Outputs(BaseWorkflow.Outputs):
        result = PromptNode.Outputs.text
```

### Usage Example

```python
from vellum import ChatMessageRequest
from .workflow import BasicRAGWorkflow
from .inputs import Inputs

# Initialize workflow
workflow = BasicRAGWorkflow()

# Execute with sample question
response = workflow.run(
    inputs=Inputs(
        chat_history=[
            ChatMessageRequest(
                role="USER",
                text="How often is employee training conducted?",
            )
        ]
    )
)

print(response.outputs.result)
```

Example output:
```
According to the Information Security Policy, employee training is conducted 
annually. All new employees must complete information security awareness 
training during onboarding and then annually thereafter. The training covers:

- Security and privacy requirements
- Correct use of information assets and facilities
- Incident response procedures
- Contingency planning

Additionally, developers working on internet-facing or customer-data applications 
must complete annual security training on:
- Secure coding practices
- OWASP secure development principles
- OWASP top 10 vulnerabilities (latest version)

Citation: Information Security Policy - v1.pdf & Software Development Life Cycle Policy - v1.pdf
```

### Next Steps

1. **Version Control**
   - Add workflow to your git repository
   - Use branch-based development for features

2. **UI Integration**
   - Continue development in the Vellum UI
   - Synchronize code changes with UI

3. **Testing**
   - Add test cases using the Evaluating RAG Pipelines guide
   - Test with various question types
   - Validate response quality

4. **Deployment**
   - Deploy to your infrastructure or Vellum's cloud
   - Set up monitoring and logging
   - Configure rate limiting and caching

This implementation provides a foundation for building more sophisticated RAG systems while maintaining clean, maintainable code. The entire solution requires less than 120 lines of code while providing enterprise-grade features like:

- Semantic search over documents
- Professional response formatting
- Source attribution
- Extensible architecture