# Defining Control Flow

This guide demonstrates common workflow patterns using the Vellum Workflows SDK.

## Single Node Workflow

The simplest possible workflow with just one node.

```ascii
●───>┌──────────┐───>●
     │StartNode │
     └──────────┘
```

```python
class MyWorkflow(BaseWorkflow):
    graph = StartNode
```

## Serial Execution Between Two Nodes

Sequential execution where output flows from one node to another.

```ascii
●───>┌──────────┐    ┌─────────┐───>●
     │StartNode │───>│ EndNode │
     └──────────┘    └─────────┘
```

```python
class MyWorkflow(BaseWorkflow):
    graph = StartNode >> EndNode
```

## Single Node Branches to Parallel Nodes

One node splitting into multiple parallel execution paths.

```ascii
                ┌──────────┐
           ┌───>│ TopNode  │────┐
┌────────┐ │    └──────────┘    │
│StartNode├─┤                    │
└────────┘ │    ┌──────────┐    │
           └───>│BottomNode│────┘
                └──────────┘
```

```python
class MyWorkflow(BaseWorkflow):
    graph = StartNode >> {
        TopNode,
        BottomNode,
    }
```

## Parallel Nodes Merging

Multiple parallel paths converging into a single node.

```ascii
                ┌──────────┐
           ┌───>│ TopNode  │────┐
┌────────┐ │    └──────────┘    │ ┌────────┐
│StartNode├─┤                    ├>│EndNode │
└────────┘ │    ┌──────────┐    │ └────────┘
           └───>│BottomNode│────┘
                └──────────┘
```

```python
class MyWorkflow(BaseWorkflow):
    graph = StartNode >> {
        TopNode,
        BottomNode,
    } >> EndNode
```

## Loops

Repeating operations until a condition is met. Common in agentic AI systems.

```ascii
●───>┌─────────┐   ┌─────┐    ┌─────────┐
     │StartNode│───>◇Port◇────[Else]────>│ExitNode │───>●
     └─────────┘    └─┬─┘     └─────────┘
          ▲           │
          └───[If]────┘
```

```python
class LoopNode(BaseNode):
    class Ports(BaseNode.Ports):
        loop = Port.on_if(Input.score.less_than(0.5))
        exit = Port.on_else()

class MyWorkflow(BaseWorkflow):
    graph = StartNode >> {
        LoopNode.Ports.loop >> StartNode,
        LoopNode.Ports.exit >> ExitNode,
    }
```

## Map Pattern

Applying the same operation to multiple items in parallel.

```ascii
                ┌──────────────────┐
                │  ┌──────────┐    │
●───────────────┤  │BaseNode │    │───────>●
                │  ├──────────┤    │
                │  │BaseNode │    │
                │  ├──────────┤    │
                │  │BaseNode │    │
                │  └──────────┘    │
                │     n=items      │
                └──────────────────┘
```

```python
@MapNode.wrap(items=Input.items)
class PromptNode(BaseNode):
    """Process each item in parallel"""
    pass

class MyWorkflow(BaseWorkflow):
    graph = PromptNode
```

## Best Practices

1. Keep workflows modular and focused on a single responsibility
2. Use clear, descriptive names for nodes and workflows
3. Consider error handling and recovery paths
4. Document complex branching logic
5. Test workflows with different input scenarios

## Related Topics

- [Configuration](/developers/workflows-sdk/configuration)
- [Core Concepts](/developers/workflows-sdk/core-concepts)
- [API Reference](/developers/workflows-sdk/api-reference)
