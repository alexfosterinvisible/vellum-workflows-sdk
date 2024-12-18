[Blog](https://www.vellum.ai/blog)[Log In](https://app.vellum.ai/)[Request Demo](https://www.vellum.ai/landing-pages/request-demo)

[Workflows SDK](/developers/workflows-sdk/introduction)[API Reference](/developers/workflows-sdk/api-reference/nodes)

# Displayable Nodes

=====================

Displayable nodes are nodes that can be displayed and edited in the Vellum UI. They support complete push and pull operations allowing you to edit the node's configuration in either the Vellum UI or as code and have those changes reflected in the other.

# Search Node

`vellum.workflows.nodes.SearchNode`

Used to perform a hybrid search against a Document Index in Vellum.

### Required Attributes
- **document_index** (`Union[UUID, str]`): Either the UUID or name of the Vellum Document Index to search against
- **query** (`str`): The query to search for

### Optional Attributes
- **options** (`SearchRequestOptionsRequest`): Runtime configuration for the search
- **chunk_separator** (`str`): The separator to use when joining the text of each search result

### Outputs
- **text** (`str`): The concatenated text output from the search
- **results** (`List[SearchResult]`): The raw results from the search

### Example Usage

```python
from vellum import (
    SearchRequestOptionsRequest,
    SearchWeightsRequest, 
    SearchResultMergingRequest,
    SearchFiltersRequest,
)
from vellum.workflows.nodes.displayable import SearchNode

class MySearchNode(SearchNode):
    query = "Hello, world"
    document_index = "my_document_index"
    options = SearchRequestOptionsRequest(
        limit=8,
        weights=SearchWeightsRequest(
            semantic_similarity=0.8,
            keywords=0.2,
        ),
        result_merging=SearchResultMergingRequest(
            enabled=True
        ),
        filters=SearchFiltersRequest(
            external_ids=None,
            metadata=None,
        ),
    )
    chunk_separator = "\n\n#####\n\n"
```

### Example Outputs

```python
from vellum import SearchResult, SearchResultDocument

MySearchNode.Outputs(
    text="Goodbye, world",
    results=[
        SearchResult(
            text="Goodbye, world",
            score=0.5,
            keywords=[...],
            document=SearchResultDocument(
                id="<id>",
                label="My Document", 
                external_id="<external-id>",
                metadata={},
            ),
            meta=None,
        ),
        ...
    ],
)
```

# Inline Prompt Node

`vellum.workflows.nodes.InlinePromptNode`

Used to execute a prompt directly within a workflow, without requiring a prompt deployment.

### Required Attributes
- **prompt_inputs** (`EntityInputsInterface`): The inputs for the Prompt
- **blocks** (`List[PromptBlock]`): The blocks that make up the Prompt
- **ml_model** (`str`): The model to use for execution (e.g., "gpt-4o", "claude-3.5-sonnet")

### Optional Attributes
- **functions** (`Optional[List[FunctionDefinition]]`): The functions to include in the prompt
- **parameters** (`Optional[PromptParameters]`): Model parameters for execution. Defaults to:
  - temperature: 0.0
  - max_tokens: 1000
  - top_p: 1.0
  - top_k: 0
  - frequency_penalty: 0.0
  - presence_penalty: 0.0
  - logitBias:
  - customParameters:
- **expand_meta** (`Optional[PromptDeploymentExpandMetaRequest]`): Expandable execution fields to include in the response
- **request_options** (`RequestOptions`): Additional options for request-specific configuration:
  - timeout_in_seconds: The number of seconds to await an API call before timing out
  - max_retries: The max number of retries to attempt if the API call fails
  - additional_headers: Additional parameters for the request's header dict
  - additional_query_parameters: Additional parameters for the request's query parameters dict
  - additional_body_parameters: Additional parameters for the request's body parameters dict

### Outputs
- **text** (`str`): The generated text output from the prompt execution
- **results** (`List[PromptOutput]`): The array of results from the prompt execution. Types include:
  - StringVellumValue
  - JsonVellumValue
  - ErrorVellumValue
  - FunctionCallVellumValue

### Example Usage

```python
from vellum.workflows.nodes import InlinePromptNode
from vellum import (
    ChatMessagePromptBlock,
    JinjaPromptBlock,
)

class MyInlinePromptNode(InlinePromptNode):
    ml_model = "gpt-4o"
    blocks = [
        ChatMessagePromptBlock(
            chat_role="SYSTEM",
            blocks=[
                JinjaPromptBlock(
                    template="""\
Answer the user's questions based on the context provided below, if you don't know the answer say "Sorry I don't know"

**Context**
``
{{ context }}
``

Limit your answer to 250 words and provide a citation at the end of your answer\
""",
                ),
            ],
        ),
        ChatMessagePromptBlock(
            chat_role="USER",
            blocks=[JinjaPromptBlock(template="{{ question }}")],
        ),
    ]
    prompt_inputs = {
        "question": "What is the best AI development platform in the world?",
        "context": "..."
    }
```

# Inline Subworkflow Node

`vellum.workflows.nodes.InlineSubworkflowNode`

Used to execute a Subworkflow defined inline within your workflow. This allows you to modularize and reuse workflow logic.

### Required Attributes
- **subworkflow** (`Type[BaseWorkflow[WorkflowInputsType, InnerStateType]]`): The Subworkflow class to execute
- **subworkflow_inputs** (`Dict[str, Any]`): The inputs to pass to the subworkflow

### Outputs
The outputs of this node are determined by the outputs defined in the subworkflow. Each output from the subworkflow will be streamed through this node.

### Example Usage

```python
from vellum.workflows.nodes import InlineSubworkflowNode
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.state import BaseState
from vellum.workflows import BaseWorkflow

class SubworkflowInputs(BaseInputs):
    query: str
    max_results: int

class SubworkflowState(BaseState):
    pass

class MySubworkflow(BaseWorkflow[SubworkflowInputs, SubworkflowState]):
    # Define your subworkflow logic here
    pass

class MyInlineSubworkflowNode(InlineSubworkflowNode):
    subworkflow = MySubworkflow
    subworkflow_inputs = {
        "query": "search term",
        "max_results": 10
    }
```

### Example Outputs

```python
MyInlineSubworkflowNode.Outputs(
    search_results=["Result 1", "Result 2", "Result 3"],
    metadata={
        "total_found": 100,
        "processing_time": 0.5
    }
)
```

# Prompt Deployment Node

`vellum.workflows.nodes.PromptDeploymentNode`

Used to execute a Prompt Deployment and surface a string output for convenience.

### Required Attributes
- **deployment** (`Union[UUID, str]`): Either the Prompt Deployment's UUID or its name
- **prompt_inputs** (`EntityInputsInterface`): The inputs for the Prompt

### Optional Attributes
- **release_tag** (`str`): The release tag to use for the Prompt Execution (Defaults to LATEST)
- **external_id** (`Optional[str]`): Unique identifier for tracking purposes
- **expand_meta** (`Optional[PromptDeploymentExpandMetaRequest]`): Expandable execution fields
- **raw_overrides** (`Optional[RawPromptExecutionOverridesRequest]`): Raw overrides for execution
- **expand_raw** (`Optional[Sequence[str]]`): Expandable raw fields to include
- **metadata** (`Optional[Dict[str, Optional[Any]]]`): Metadata for the Prompt Execution
- **request_options** (`Optional[RequestOptions]`): Request options for execution

### Outputs
- **text** (`str`): The generated text output from the prompt execution
- **results** (`List[PromptOutput]`): Array of results from execution. Types include:
  - StringVellumValue
  - FunctionCallVellumValue

### Example Usage

```python
from vellum.workflows.nodes import PromptDeploymentNode
from vellum.client import PromptDeploymentExpandMetaRequest, RawPromptExecutionOverridesRequest

class MyPromptDeploymentNode(PromptDeploymentNode):
    deployment = "my_prompt_deployment"
    prompt_inputs = {
        "question": "What is the meaning of life?",
        "chat_history": [
            ChatMessage(role="USER", text="Hello!"),
            ChatMessage(role="ASSISTANT", text="Hi there!"),
        ],
        "context": {
            "source": "philosophy_book",
            "chapter": 42
        }
    }
    release_tag = "production"
    external_id = "unique-execution-id"
    expand_meta = PromptDeploymentExpandMetaRequest(
        model_name=True,
        usage=True,
        cost=True,
        finish_reason=True,
        latency=True,
        deployment_release_tag=True,
        prompt_version_id=True
    )
    metadata = {
        "user_id": "123",
        "session_id": "abc"
    }
```

### Example Outputs

```python
MyPromptDeploymentNode.Outputs(
    text="happily",
    results=[
        StringVellumValue(value="h"),
        StringVellumValue(value="app"),
        StringVellumValue(value="ily"),
    ]
)
```

# Subworkflow Deployment Node

`vellum.workflows.nodes.SubworkflowDeploymentNode`

Used to execute a deployed Workflow as a subworkflow within another workflow. This allows you to compose workflows from other deployed workflows.

### Required Attributes
- **deployment** (`Union[UUID, str]`): Either the Workflow Deployment's UUID or its name
- **subworkflow_inputs** (`Dict[str, Any]`): The inputs for the Subworkflow. Supports:
  - Strings
  - Numbers (float)
  - Chat History (List[ChatMessage])
  - JSON objects (Dict[str, Any])

### Optional Attributes
- **release_tag** (`str`): The release tag to use for the Workflow Execution (Defaults to LATEST)
- **external_id** (`Optional[str]`): The external ID to use for the Workflow Execution
- **expand_meta** (`Optional[WorkflowExpandMetaRequest]`): Configuration for including additional metadata
- **metadata** (`Optional[Dict[str, Optional[Any]]]`): The metadata to use for the Workflow Execution
- **request_options** (`Optional[RequestOptions]`): The request options to use for the Workflow Execution

### Outputs
The outputs of this node are determined by the outputs defined in the deployed workflow. Each output from the workflow will be streamed through this node.

### Example Usage

```python
from vellum import ChatMessage, WorkflowExpandMetaRequest
from vellum.workflows.nodes import SubworkflowDeploymentNode

class MySubworkflowNode(SubworkflowDeploymentNode):
    deployment = "customer_support_workflow"  # or UUID("...")
    subworkflow_inputs = {
        "user_query": "How do I reset my password?",
        "chat_history": [
            ChatMessage(role="USER", text="Hi there"),
            ChatMessage(role="ASSISTANT", text="Hello! How can I help?")
        ],
        "user_metadata": {
            "user_id": "123",
            "account_type": "premium"
        },
        "priority_score": 0.8
    }
    release_tag = "production"
    external_id = "support-ticket-456"
    expand_meta = WorkflowExpandMetaRequest(
        include_inputs=True,
        include_outputs=True
    )
    metadata = {
        "source": "mobile_app",
        "region": "us-west"
    }
```

### Example Output Stream

```python
# Outputs are streamed as they're generated by the workflow
for output in node.run():
    if output.is_streaming:
        print(f"Received partial output for {output.name}: {output.delta}")
    elif output.is_fulfilled:
        print(f"Received final output for {output.name}: {output.value}")
```

# API Node

`vellum.workflows.nodes.APINode`

Used to make HTTP requests to external APIs.

### Required Attributes
- **url** (`str`): The URL to send the request to
- **method** (`APIRequestMethod`): The HTTP method to use for the request

### Optional Attributes
- **headers** (`Optional[Dict[str, Union[str, VellumSecret]]]`): The headers to send in the request
- **data** (`Optional[str]`): The data to send in the request body
- **json** (`Optional[JsonObject]`): The JSON data to send in the request body
- **authorization_type** (`Optional[AuthorizationType]`): The type of authorization to use
- **api_key_header_key** (`Optional[str]`): The header key to use for API key authorization
- **bearer_token_value** (`Optional[str]`): The bearer token value to use for bearer token authorization

### Outputs
- **status_code** (`int`): The HTTP status code of the response
- **headers** (`Dict[str, str]`): The response headers
- **text** (`str`): The raw text response body
- **json** (`Optional[Dict[str, Any]]`): The parsed JSON response body (if the response is JSON)

### Example Usage

```python
from vellum.workflows.nodes import APINode

class MyAPINode(APINode):
    url = "https://api.example.com/data"
    method = "POST"
    headers = {
        "Authorization": "Bearer ${secrets.API_KEY}",
        "Content-Type": "application/json"
    }
    json = {
        "query": "example",
        "filters": {
            "category": "books",
            "limit": 10
        }
    }
```

# Code Execution Node

`vellum.workflows.nodes.CodeExecutionNode`

Used to execute arbitrary Python code within your workflow. Supports custom package dependencies and any Python or TypeScript runtimes.

### Required Attributes
- **filepath** (`str`): Path to the Python script file to execute
- **code_inputs** (`EntityInputsInterface`): The inputs for the custom script. Supports:
  - Strings
  - Numbers (float)
  - Arrays
  - Chat History (List[ChatMessage])
  - Search Results (List[SearchResult])
  - JSON objects (Dict[str, Any])
  - Function Calls
  - Errors
  - Secrets

### Optional Attributes
- **runtime** (`CodeExecutionRuntime`): The runtime to use (Defaults to PYTHON_3_12)
- **packages** (`Optional[Sequence[CodeExecutionPackage]]`): The packages to use
- **request_options** (`Optional[RequestOptions]`): The request options to use

### Outputs
- **result** (`_OutputType`): The result returned by the executed code
- **log** (`str`): The execution logs from the code run

### Example Usage

```python
from vellum.workflows.nodes import CodeExecutionNode
from vellum import ChatMessage, CodeExecutionPackage
from vellum.workflows.state import BaseState
from typing import List, Dict

class MyCodeExecutionNode(CodeExecutionNode[BaseState, Dict[str, Any]]):
    filepath = "./scripts/process_data.py"
    code_inputs = {
        "text": "Process this text",
        "chat_history": [
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi there!")
        ],
        "config": {
            "max_length": 100,
            "temperature": 0.7
        }
    }
    runtime = "PYTHON_3_11_6"
    packages = [
        CodeExecutionPackage(name="pandas", version="2.0.0"),
        CodeExecutionPackage(name="numpy", version="1.24.0")
    ]
```

### Example Outputs

```python
MyCodeExecutionNode.Outputs(
    result={
        "processed_text": "PROCESS THIS TEXT",
        "history_length": 2,
        "config_used": {
            "max_length": 100,
            "temperature": 0.7
        }
    },
    log="INFO: Starting processing...\nINFO: Processing complete"
)
```

# Templating Node

`vellum.workflows.nodes.TemplatingNode`

Used to render text templates using Jinja2 syntax.

### Required Attributes
- **template** (`str`): The Jinja2 template to render
- **inputs** (`EntityInputsInterface`): The values to substitute into the template

### Outputs
- **result** (`_OutputType`): The rendered template in the appropriate type as specified by the Templating Node subclass definition

### Example Usage

```python
from vellum.workflows.nodes import TemplatingNode

# Note: `str` is the default output type for the Templating Node
class MyTemplatingNode(TemplatingNode[BaseState, str]):
    template = "The weather in {{ city }} is {{ weather }}."
    inputs = {
        "city": Inputs.city,
        "weather": Inputs.weather,
    }
```

### Example Outputs

```python
MyTemplatingNode.Outputs(
    result="""
    Dear Jane Doe,
    
    Thank you for your 5 years of service at Acme Corp.
    Your dedication to Engineering has been invaluable.
    
    Best regards,
    HR Team
    """
)
```

# Guardrail Node

`vellum.workflows.nodes.GuardrailNode`

Used to execute a Metric Definition and surface a float output representing the score. This node is commonly used to implement quality checks and guardrails in your workflows.

### Required Attributes
- **metric_definition** (`Union[UUID, str]`): Either the Metric Definition's UUID or its name
- **metric_inputs** (`EntityInputsInterface`): The inputs for the Metric

### Optional Attributes
- **release_tag** (`str`): The release tag to use (Defaults to LATEST)
- **request_options** (`Optional[RequestOptions]`): Request options for execution

### Outputs
- **score** (`float`): The score output from the metric execution (between 0 and 1)
- Additional outputs may be available depending on the metric definition

### Example Usage

```python
from vellum import ChatMessage
from vellum.workflows.nodes import GuardrailNode

class QualityCheckNode(GuardrailNode):
    release_tag = "production"
    metric_definition = "response_quality_metric"  # or UUID("...")
    metric_inputs = {
        "response": "This is the AI response to evaluate",
        "chat_history": [
            ChatMessage(role="USER", text="What's the weather?"),
            ChatMessage(role="ASSISTANT", text="It's sunny today!")
        ],
        "evaluation_criteria": {
            "coherence": True,
            "relevance": True,
            "safety": True
        }
    }
```

### Example Outputs

```python
QualityCheckNode.Outputs(
    # score is mandatory for all Metrics
    score=0.92,
    # details is from our custom Metric definition
    details={
        "coherence_score": 0.95,
        "relevance_score": 0.88,
        "safety_score": 0.93
    }
)
```

# Map Node

`vellum.workflows.nodes.MapNode`

Used to map over a list of items and execute a Subworkflow for each item. This enables parallel processing of multiple items through the same workflow logic.

### Required Attributes
- **items** (`List[Any]`): The list of items to map over
- **subworkflow** (`Type[BaseWorkflow[WorkflowInputsType, InnerStateType]]`): The Subworkflow class to execute for each item

### Optional Attributes
- **concurrency** (`Optional[int]`): Maximum number of concurrent subworkflow executions (Defaults to None)

### Outputs
The outputs are determined by the subworkflow's outputs, with each output field becoming a list containing results from all iterations.

### Example Usage

```python
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.state import BaseState
from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes import MapNode, BaseNode
from typing import List

class MapNodeInputs(BaseInputs):
    my_list: List[str]

class Iteration(BaseNode):
    item = MapNode.SubworkflowInputs.item
    index = MapNode.SubworkflowInputs.index

    class Outputs(BaseNode.Outputs):
        result: str

    def run(self) -> Outputs:
        return self.Outputs(result=self.item + str(self.index))
    
class IterationSubworkflow(BaseWorkflow[MapNode.SubworkflowInputs, BaseState]):
    graph = Iteration

    class Outputs(BaseWorkflow.Outputs):
        result = Iteration.Outputs.result

class MyMapNode(MapNode):
    items = MapNodeInputs.my_list
    subworkflow = IterationSubworkflow

    class Outputs(BaseNode.Outputs):
        result: List[str]  # Must match the Subworkflow's Outputs.result attribute
```

### Example Outputs

```python
MyMapNode.Outputs(
    result=[
        "text0",
        "text1",
        "text2"
    ]
)
```

# Conditional Node

`vellum.workflows.nodes.ConditionalNode`

Used to conditionally determine which port to invoke next. This node exists for backwards compatibility with Vellum's Conditional Node. For most cases, you should extend `BaseNode.Ports` directly.

### Example Usage

```python
from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes import BaseNode
from vellum.workflows.state import BaseState

class SourceNode(BaseNode):
    pass

class MiddleNode(BaseNode):
    class Ports(BaseNode.Ports):
        top = Port.on_if(SourceNode.Execution.count.less_than(1))
        bottom = Port.on_else()

class TargetNode(BaseNode):
    pass

class MyWorkflow(BaseWorkflow):
    graph = SourceNode >> {
        # Execute SourceNode one more time before TargetNode
        MiddleNode.Ports.top >> SourceNode,
        MiddleNode.Ports.bottom >> TargetNode,
    }

    class Outputs(BaseWorkflow.Outputs):
        result = TargetNode.Outputs
```

# Merge Node

`vellum.workflows.nodes.MergeNode`

Used to merge the control flow of multiple nodes into a single node. This node exists primarily for backwards compatibility. For most cases, you should extend from `BaseNode.Trigger` directly.

### Example Usage

```python
from vellum.workflows.nodes import BaseNode

class QuickNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        prefix = "Hello"

class SlowNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        suffix: str
    def run(self) -> Outputs:
        time.sleep(5)
        return self.Outputs(suffix="World")

class MergeNode(BaseNode):
    prefix = QuickNode.Outputs.prefix
    suffix = SlowNode.Outputs.suffix
    
    class Outputs(BaseNode.Outputs):
        message: str
    
    class Trigger(BaseNode.Trigger):
        merge_strategy = MergeStrategy.AWAIT_ALL
    
    def run(self) -> Outputs:
        return self.Outputs(message=f"{self.prefix} {self.suffix}")
```

# Error Node

`vellum.workflows.nodes.ErrorNode`

Used to raise an error to reject the surrounding Workflow and return custom error messages.

### Required Attributes
- **error** (`Union[str, VellumError]`): The error to raise. Can be either:
  - A string message
  - A VellumError object with a `message` and error `code`

### Example Usage

```python
from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes import ErrorNode
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.state import BaseState

class Inputs(BaseInputs):
    threshold: int

class StartNode(BaseNode):
    class Ports(BaseNode.Ports):
        success = Port.on_if(Inputs.threshold.greater_than(10))
        fail = Port.on_else()

class SuccessNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result = Inputs.threshold

class FailNode(ErrorNode):
    error = "Input threshold was too low"

class BasicErrorNodeWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = {
        StartNode.Ports.success >> SuccessNode,
        StartNode.Ports.fail >> FailNode,
    }
    class Outputs(BaseWorkflow.Outputs):
        final_value = SuccessNode.Outputs.result
```

# Final Output Node

`vellum.workflows.nodes.FinalOutputNode`

Used to directly reference the output of another node. This provides backward compatibility with Vellum's Final Output Node functionality. In most cases, you should reference the Workflow Output directly to the output of a particular node.

### Required Attributes
- **value** (`_OutputType`): The value to be output

### Outputs
- **value** (`_OutputType`): The output value, with the same type as the input value

### Example Usage

```python
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.state import BaseState
from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes import FinalOutputNode

class Inputs(BaseInputs):
    input: str

class BasicFinalOutputNode(FinalOutputNode):
    class Outputs(FinalOutputNode.Outputs):
        value = Inputs.input

class BasicFinalOutputNodeWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = BasicFinalOutputNode

    class Outputs(BaseWorkflow.Outputs):
        value = BasicFinalOutputNode.Outputs.value
```

