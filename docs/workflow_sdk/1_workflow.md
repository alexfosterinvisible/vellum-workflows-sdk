# Workflows SDK Core Concepts

## Table of Contents
1. [Defining a Workflow](#defining-a-workflow)
2. [Workflow Outputs](#workflow-outputs)
3. [Defining Nodes](#defining-nodes)
4. [Using Nodes in Workflows](#using-nodes-in-workflows)
5. [Workflow Inputs](#workflow-inputs)
6. [Control Flow](#control-flow)
7. [Ports and Conditionals](#ports-and-conditionals)
8. [Expressions](#expressions)
9. [Triggers](#triggers)
10. [Parallel Execution](#parallel-execution)
11. [State Management](#state-management)
12. [Streaming Outputs](#streaming-outputs)

## Defining a Workflow

All Vellum Workflows extend from the `BaseWorkflow` class. Workflows define the control flow of your application, orchestrating the order of execution between each Node.

Workflows can be invoked via a `run` method, which returns the final event that was emitted by the Workflow.

```python
class MyWorkflow(BaseWorkflow):
    pass

workflow = MyWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
```

In the example above, `final_event` has a name of "workflow.execution.fulfilled". This indicates that the Workflow ran to completion successfully. Had the Workflow encountered an error, the name would have been "workflow.execution.rejected".

## Workflow Outputs

You can think of a Workflow as a black box that produces values for pre-defined outputs. To specify the outputs of a Workflow, you must define an `Outputs` class that extends from `BaseWorkflow.Outputs`.

```python
class MyWorkflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        greeting = "Hello, world!"

workflow = MyWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.greeting == "Hello, world!"
```

## Defining Nodes

Nodes are the building blocks of a Workflow and are responsible for executing a specific task. All Nodes in a Workflow must extend from the `BaseNode` class.

```python
class GreetingNode(BaseNode):
    def run(self) -> BaseNode.Outputs:
        print("Hello, world!")
        return self.Outputs()
```

### Defining Node Outputs

Most Nodes produce Outputs that can be referenced elsewhere in the Workflow. Just like a Workflow, a Node defines its outputs via an `Outputs` class, extending from `BaseNode.Outputs`.

```python
class GreetingNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        greeting: str
        
    def run(self) -> BaseNode.Outputs:
        greeting = "Hello, world!"
        print(greeting)
        return self.Outputs(greeting=greeting)
```

## Using Nodes in Workflows

Nodes are executed as part of a Workflow once they're added to the Workflow's `graph` attribute. Once added, a Node's output can be used as the Workflow's output.

```python
class GreetingNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        greeting: str
        
    def run(self) -> BaseNode.Outputs:
        greeting = "Hello, world!"
        print(greeting)
        return self.Outputs(greeting=greeting)

class MyWorkflow(BaseWorkflow):
    # Add the GreetingNode to the Workflow's graph
    graph = GreetingNode
    
    class Outputs(BaseWorkflow.Outputs):
        # Use the GreetingNode's output as the Workflow's output
        greeting = GreetingNode.Outputs.greeting  

workflow = MyWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.greeting == "Hello, world!"
```

## Workflow Inputs

The runtime behavior of a Workflow almost always depends on some set of input values that are provided at the time of execution.

You can define a Workflow's inputs via an `Inputs` class that extends from `BaseInputs` and that's then referenced in the Workflow's parent class as a generic type.

```python
class Inputs(BaseInputs):
    greeting: str

class MyWorkflow(BaseWorkflow[Inputs, BaseState]):
    class Outputs(BaseWorkflow.Outputs):
        greeting = Inputs.greeting

workflow = MyWorkflow()
final_event = workflow.run(inputs=Inputs(greeting="Hello, world!"))
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.greeting == "Hello, world!"
```

### Node Attributes

A Workflow's inputs are usually used to drive the behavior of its Nodes. Nodes can reference these inputs via class attributes that are resolved at runtime.

```python
class Inputs(BaseInputs):
    noun: str

class GreetingNode(BaseNode):
    noun = Inputs.noun
    
    class Outputs(BaseNode.Outputs):
        greeting: str
        
    def run(self) -> Outputs:
        return self.Outputs(greeting=f"Hello, {self.noun}!")

class MyWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = GreetingNode
    
    class Outputs(BaseWorkflow.Outputs):
        hello = GreetingNode.Outputs.greeting

workflow = MyWorkflow()
# Run it once with "world"
final_event = workflow.run(inputs=Inputs(noun="world"))
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.hello == "Hello, world!"

# Run it again with "universe"
final_event = workflow.run(inputs=Inputs(noun="universe"))
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.hello == "Hello, universe!"
```

> **Note**: `Inputs.noun` is what we call a "descriptor" and is not a literal value. Think of it like a pointer or reference whose value is resolved at runtime. If you were to call `Inputs.noun` within a node's run method instead of `self.noun` an exception would be raised.

## Control Flow

### Defining Control Flow

Until now, we've only defined Workflows that contain a single Node – not very interesting! Most Workflows orchestrate the execution of multiple Nodes in a specific order. This is achieved by defining a `graph` attribute with a special syntax that describes the control flow between Nodes.

```python
class MyWorkflow(BaseWorkflow):
    graph = GreetingNode >> EndNode >> AggregatorNode
    
    class Outputs(BaseWorkflow.Outputs):
        results = AggregatorNode.Outputs.results

workflow = MyWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.results == ["Hello, world!", "Goodbye, world!"]
```

## Ports and Conditionals

Nodes contain Ports and use them to determine which Nodes to execute next. Ports are useful for performing branching logic and conditional execution of subsequent Nodes.

```python
class SwitchNode(BaseNode):
    class Ports(BaseNode.Ports):
        # Invoke the `winner` Port if the `StartNode`'s `score` output is greater than `5`
        winner = Port.on_if(StartNode.Outputs.score.greater_than(5))
        # Otherwise, invoke the `loser` Port
        loser = Port.on_else()

class MyWorkflow(BaseWorkflow):
    graph = StartNode >> {
        SwitchNode.Ports.winner >> WinnerNode,
        SwitchNode.Ports.loser >> LoserNode,
    }
    
    class Outputs(BaseWorkflow.Outputs):
        result = WinnerNode.Outputs.result.coalesce(LoserNode.Ports.result)

workflow = MyWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.result in ("We won!", "We lost :(")
```

## Expressions

Descriptors support a declarative syntax for defining Expressions. Expressions are usually used in conjunction with Ports to define conditional execution of subsequent Nodes, but can also be used as short-hand for performing simple operations.

```python
# Longform definition
class EndNode(BaseNode):
    score = StartNode.Outputs.score
    
    class Outputs(BaseNode.Outputs):
        winner: bool
        
    def run(self) -> Outputs:
        return self.Outputs(winner=self.score > 5)

# Shortform using Expression
class EndNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        winner = StartNode.Outputs.score.greater_than(5)
```

## Triggers

Triggers control when a Node should execute based on its dependencies. By default, a Node will execute as soon as any one of its immediately upstream Nodes have fulfilled.

```python
class MergeNode(BaseNode):
    prefix = QuickNode.Outputs.prefix
    suffix = SlowNode.Outputs.suffix
    
    class Outputs(BaseNode.Outputs):
        message: str
        
    class Trigger(BaseNode.Trigger):
        merge_strategy = MergeStrategy.AWAIT_ALL
        
    def run(self) -> Outputs:
        return self.Outputs(message=f"{self.prefix} {self.suffix}")

class MyWorkflow(BaseWorkflow):
    graph = {
        QuickNode,
        SlowNode,
    } >> MergeNode
    
    class Outputs(BaseWorkflow.Outputs):
        result = MergeNode.Outputs.message
```

## Parallel Execution

You can run multiple execution paths in parallel using "set syntax":

```python
class BasicParallelizationWorkflow(BaseWorkflow):
    graph = StartNode >> {
        FirstNode,
        SecondNode,
    }
    
    class Outputs(BaseWorkflow.Outputs):
        first_node_time: int = FirstNode.Outputs.total_time
        second_node_time: int = SecondNode.Outputs.total_time
```

## State Management

Workflows support writing to and reading from a global state object that lives for the duration of the Workflow's execution.

```python
class State(BaseState):
    items: Set[int]

class TopNode(BaseNode[State]):
    def run(self) -> BaseNode.Outputs:
        self.state.items.add(random.randint(0, 10))
        return self.Outputs()

class BottomNode(BaseNode[State]):
    def run(self) -> BaseNode.Outputs:
        self.state.items.add(random.randint(10, 20))
        return self.Outputs()

class MergeNode(BaseNode):
    all_items = State.items
    
    class Outputs(BaseNode.Outputs):
        total: int
        
    class Trigger(BaseNode.Trigger):
        merge_strategy = MergeStrategy.AWAIT_ALL
        
    def run(self) -> Outputs:
        return self.Outputs(total=len(self.state.all_items))

class MyWorkflow(BaseWorkflow[BaseInputs, State]):
    graph = {
        TopNode,
        BottomNode,
    } >> MergeNode
    
    class Outputs(BaseWorkflow.Outputs):
        result = MergeNode.Outputs.total
```

## Streaming Outputs

### Workflow Event Streaming

You can stream events from a Workflow as they're being emitted using the `stream()` method:

```python
workflow = MyWorkflow()
events = workflow.stream(inputs=Inputs(boost=10))

for event in events:
    if event.name == "workflow.execution.initiated":
        assert event.inputs.boost == 10
    elif event.name == "workflow.execution.fulfilled":
        assert event.outputs.winner is True
    elif event.name == "workflow.execution.streaming":
        if event.output.name == "score":
            assert event.output.value > 10
        elif event.output.name == "winner":
            assert event.output.value is True
```

### Node Event Streaming

You can also receive Node-level events by specifying the `event_types` parameter:

```python
events = workflow.stream(
    inputs=Inputs(boost=10),
    event_types={
        WorkflowEventType.NODE,
        WorkflowEventType.WORKFLOW,
    },
)

for event in events:
    if event.name == "workflow.execution.initiated":
        assert event.inputs.boost == 10
    elif event.name == "workflow.execution.fulfilled":
        assert event.outputs.winner is True
    elif event.name == "node.execution.fulfilled":
        if event.node_class is StartNode:
            assert event.outputs.score > 10
        elif event.node_class is EndNode:
            assert event.outputs.winner is True
```
