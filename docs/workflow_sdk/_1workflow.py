"""Vellum Workflows Quickstart Guide

CONTENTS:
1. Basic Workflow Example
   - Simple node and workflow definition
   - Basic output handling

2. Workflow Execution Status
   - Understanding workflow execution states
   - Fulfilled vs rejected states

3. Workflow Outputs
   - Defining workflow outputs
   - Output class inheritance

4. Basic Nodes
   - Node definition and structure
   - Simple node execution

5. Nodes with Outputs
   - Adding outputs to nodes
   - Node output integration

6. Workflow Inputs
   - Input handling in workflows
   - Input class definition

7. Node Attributes
   - Using workflow inputs in nodes
   - Dynamic node behavior

8. Control Flow
   - Sequential node execution
   - Node chaining and dependencies

9. Parallel Execution
   - Concurrent node execution
   - Parallel workflow patterns

10. State Management
    - Workflow state handling
    - State sharing between nodes
"""


# https://docs.vellum.ai/developers/workflows-sdk/core-concepts
# The Vellum Workflows SDK provides a declarative Python syntax for both defining and executing the control flow of graphs. Unlike other graph execution frameworks, which are functional or event-driven in nature, Vellum’s Workflows SDK defines the control flow of a graph statically and makes use of strict typing. This means that the structure of the graph is known ahead of time, and you get all the benefits of type safety and intellisense. This ultimately makes it easier to build more predictable and robust AI systems.

# Unique amongst other frameworks, Vellum’s Workflows SDK also allows you to visualize, edit, and execute your graph in a UI, pushing and pulling changes from code to UI and vice versa.

# Open Source
# The Vellum Workflows SDK is open source and publicly available on GitHub. See source code here.

# Core Features
# Nodes: Nodes are the basic building blocks of a graph. They represent a single task or function.
# Graph Syntax: An intuitive, declarative syntax for defining the control flow of a graph.
# Inputs and Outputs: Both the Workflow itself and individual Nodes can take in inputs and produce outputs, which can be used to pass information between Nodes or Workflows.
# State: Nodes can read and write to the graph’s global state, which can be used to share information between Nodes without defining explicit inputs and outputs.
# Advanced Control Flow: Support for looping, conditionals, paralellism, state forking, and more.
# Streaming: Nodes can stream output values back to the runner, allowing for long-running tasks like chat completions to return partial results.
# Human-in-the-loop: Nodes can wait for External Inputs, allowing for a pause in the Workflow until a human or external system provides input.
# UI Integration: Push and pull changes from code to Vellum’s UI and vice versa, allowing for rapid testing and iteration.


# --------------------------------------------------------
# Imports
# --------------------------------------------------------
from typing import Set
import random
import time
from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes import BaseNode
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.state import BaseState
from vellum.workflows.nodes.trigger import MergeStrategy

# --------------------------------------------------------
# Basic Workflow Example
# --------------------------------------------------------


class MyNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result: str

    def run(self):
        return self.Outputs(result="Hello, World!")


class MyWorkflow(BaseWorkflow):
    graph = MyNode

    class Outputs(BaseWorkflow.Outputs):
        result = MyNode.Outputs.result

# --------------------------------------------------------
# Workflow Execution Status
# --------------------------------------------------------


class MyWorkflow(BaseWorkflow):
    pass


workflow = MyWorkflow()
final_event = workflow.run()

print(f"final_event.name: {final_event.name}")
assert final_event.name == "workflow.execution.fulfilled"
print("\nWorkflow execution status:")
print("---------------------------")
print("When a workflow completes successfully, the final event name is 'workflow.execution.fulfilled'")
print("When a workflow encounters an error, the final event name is 'workflow.execution.rejected'")
print(f"\nIn this case, the final event name was: {final_event.name}")
print("---------------------------\n")

# --------------------------------------------------------
# Workflow Outputs
# --------------------------------------------------------
print("\nWorkflow Outputs:")
print("---------------------------")
print("Workflows can produce values for pre-defined outputs")
print("To specify outputs, define an Outputs class extending BaseWorkflow.Outputs")
print("Below is a basic workflow with a single output 'greeting' set to 'Hello, world!'")
print("---------------------------\n")


class MyWorkflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        greeting = "Hello, world!"


workflow = MyWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.greeting == "Hello, world!"

print(f"final_event.outputs.greeting: {final_event.outputs.greeting}")
print("---------------------------\n")

# --------------------------------------------------------
# Basic Nodes
# --------------------------------------------------------
print("\nDefining Basic Nodes:")
print("---------------------------")
print("Nodes are building blocks that execute specific tasks")
print("Below is a simple GreetingNode that just prints a message")
print("---------------------------\n")


class GreetingNode(BaseNode):
    def run(self) -> BaseNode.Outputs:
        print("Hello, world!")
        return self.Outputs()


class BasicNodeWorkflow(BaseWorkflow):
    graph = GreetingNode

    class Outputs(BaseWorkflow.Outputs):
        pass


workflow = BasicNodeWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"

# --------------------------------------------------------
# Nodes with Outputs
# --------------------------------------------------------
print("\nNode with Outputs:")
print("---------------------------")
print("Nodes can produce outputs via an Outputs class")
print("Below we add a 'greeting' output to our node")
print("---------------------------\n")


class GreetingNodeWithOutput(BaseNode):
    class Outputs(BaseNode.Outputs):
        greeting: str

    def run(self) -> BaseNode.Outputs:
        greeting = "Hello, world!"
        print(f"Node producing output: {greeting}")
        return self.Outputs(greeting=greeting)


class OutputWorkflow(BaseWorkflow):
    graph = GreetingNodeWithOutput

    class Outputs(BaseWorkflow.Outputs):
        greeting = GreetingNodeWithOutput.Outputs.greeting


workflow = OutputWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
print(f"Workflow output: {final_event.outputs.greeting}")
print("---------------------------\n")

# --------------------------------------------------------
# Workflow Inputs
# --------------------------------------------------------
print("\nWorkflow Inputs:")
print("---------------------------")
print("Workflows can accept inputs that affect their behavior")
print("Below we create a workflow that takes a 'greeting' input")
print("---------------------------\n")


class Inputs(BaseInputs):
    greeting: str


class InputWorkflow(BaseWorkflow[Inputs, BaseState]):
    class Outputs(BaseWorkflow.Outputs):
        greeting = Inputs.greeting


workflow = InputWorkflow()
final_event = workflow.run(inputs=Inputs(greeting="Hello from inputs!"))
assert final_event.name == "workflow.execution.fulfilled"
print(f"Workflow with input: {final_event.outputs.greeting}")

# --------------------------------------------------------
# Node Attributes
# --------------------------------------------------------
print("\nNode Attributes:")
print("---------------------------")
print("Nodes can use workflow inputs via attributes")
print("Below we create a node that uses the input to create a dynamic greeting")
print("---------------------------\n")


class DynamicInputs(BaseInputs):
    noun: str


class DynamicGreetingNode(BaseNode):
    noun = DynamicInputs.noun

    class Outputs(BaseNode.Outputs):
        greeting: str

    def run(self) -> Outputs:
        return self.Outputs(greeting=f"Hello, {self.noun}!")


class DynamicWorkflow(BaseWorkflow[DynamicInputs, BaseState]):
    graph = DynamicGreetingNode

    class Outputs(BaseWorkflow.Outputs):
        hello = DynamicGreetingNode.Outputs.greeting


workflow = DynamicWorkflow()

# Run with "world"
final_event = workflow.run(inputs=DynamicInputs(noun="world"))
assert final_event.name == "workflow.execution.fulfilled"
print(f"Dynamic greeting 1: {final_event.outputs.hello}")

# Run with "universe"
final_event = workflow.run(inputs=DynamicInputs(noun="universe"))
assert final_event.name == "workflow.execution.fulfilled"
print(f"Dynamic greeting 2: {final_event.outputs.hello}")
print("---------------------------\n")

# --------------------------------------------------------
# Control Flow
# --------------------------------------------------------
print("\nControl Flow:")
print("---------------------------")
print("Here's a more complex control flow example with multiple nodes")
print("---------------------------\n")

# workflow.py


class MyWorkflow(BaseWorkflow):
    graph = GreetingNode >> SalutationNode >> AggregatorNode

    class Outputs(BaseWorkflow.Outputs):
        results = AggregatorNode.Outputs.results

# nodes/greeting.py


class GreetingNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        greeting: str

    def run(self) -> Outputs:
        return self.Outputs(greeting=f"Hello, world!")

# nodes/salutation.py


class SalutationNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        salutation: str

    def run(self) -> Outputs:
        return self.Outputs(salutation="Goodbye, world!")

# nodes/aggregator.py


class AggregatorNode(BaseNode):
    greeting = GreetingNode.Outputs.greeting
    salutation = SalutationNode.Outputs.salutation

    class Outputs(BaseNode.Outputs):
        results: list[str]

    def run(self) -> Outputs:
        return self.Outputs(results=[self.greeting, self.salutation])


workflow = MyWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.results == ["Hello, world!", "Goodbye, world!"]
print(f"Control flow results: {final_event.outputs.results}")
print("---------------------------\n")


# --------------------------------------------------------
# Ports and Conditionals
# --------------------------------------------------------
print("\nPorts and Conditionals:")
print("---------------------------")
print("Nodes contain Ports and use them to determine which Nodes to execute next.")
print("Ports are useful for performing branching logic and conditional execution of subsequent Nodes.")
print("We haven’t seen any Ports up until now, but they’re actually present in every Node.")
print("By default, a Node has a single Port called default, which is always invoked after the Node’s run method completes.")

print("The following Workflows are equivalent:")
print("---------------------------\n")


class MyWorkflow1(BaseWorkflow):
    graph = GreetingNode >> SomeNode,

    class Outputs(BaseWorkflow.Outputs):
        result = "Hello"


class MyWorkflow2(BaseWorkflow):
    graph = GreetingNode.Ports.default >> WinnerNode,

    class Outputs(BaseWorkflow.Outputs):
        result = "Hello"

# You can explicitly define a Ports class on a Node and define the conditions in which one Node or another should execute.
# Below, we define a SwitchNode that has a winner Port and a loser Port.

# workflow.py


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

# nodes/start_node.py


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        score: int

    def run(self) -> Outputs:
        return self.Outputs(score=random.randint(0, 10))


# nodes/winner_node.py
class WinnerNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result = "We won!"

# nodes/loser_node.py


class LoserNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result = "We lost :("


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

# Notice that we use the greater_than Expression to define the winner Port— more on Expressions next.

print(f"Final event result: {final_event.outputs.result}")
print("---------------------------\n")

# --------------------------------------------------------
# Triggers
# --------------------------------------------------------
print("\nTriggers:")
print("---------------------------")
print("In some cases, you may want to delay the execution of a Node until a certain condition is met.")
print("For example, you may want to wait for multiple upstream Nodes to complete before executing a Node, like when executing Nodes in parallel.")
print("This is where Triggers come in.")
print("---------------------------\n")

print("Just as Nodes define a Ports class implicitly by default, they also define a Trigger class implicitly by default.")
print("Here’s what the default Trigger class looks like:")
print("---------------------------\n")


class Trigger(BaseNode.Trigger):
    merge_behavior = MergeStrategy.AWAIT_ANY


print("This means that by default, a Node will execute as soon as any one of its immediately upstream Nodes have fulfilled.")
print("You might instead want to wait until all of its upstream Nodes have fulfilled.")
print("To do this, you can explicitly define a Trigger class on a Node like so:")
print("---------------------------\n")


class Trigger(BaseNode.Trigger):
    merge_behavior = MergeStrategy.AWAIT_ALL


print("Here’s a complete example:")
print("---------------------------\n")


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


class MyWorkflow(BaseWorkflow):
    graph = {
        QuickNode,
        SlowNode,
    } >> MergeNode

    class Outputs(BaseWorkflow.Outputs):
        result = MergeNode.Outputs.message


workflow = MyWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.result == "Hello World"

# It’s usually sufficient to stick with the “Await All” and “Await Any” merge behaviors that are provided out-of-box.
# However, you can also define your own custom merge behaviors by overriding the Trigger class’s should_initiate method.
# By doing so, you can access any information about the Node’s dependencies or the Workflow’s State (more on State later).

# --------------------------------------------------------
# Parallel Execution
# --------------------------------------------------------
print("\nParallel Execution:")
print("---------------------------")
print("Nodes can be executed in parallel using set syntax {}")
print("Below we run two nodes concurrently")
print("---------------------------\n")
# Parallel Execution
# You may want to run multiple execution paths in parallel. For example, if you want to run multiple LLM prompts concurrently, or respond to a user while performing background tasks. To do this, you can use “set syntax” as follows:


# workflow_parallelized.py
class FirstNode(TimeSinceStartNode):
    pass


class SecondNode(TimeSinceStartNode):
    pass


class BasicParallelizationWorkflow(BaseWorkflow):
    graph = StartNode >> {
        FirstNode,
        SecondNode,
    }

    class Outputs(BaseWorkflow.Outputs):
        first_node_time: int = FirstNode.Outputs.total_time
        second_node_time: int = SecondNode.Outputs.total_time


workflow = BasicParallelizationWorkflow()
final_event = workflow.run()

assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.first_node_time == 1
assert final_event.outputs.second_node_time == 1


# workflow_sequential.py
class FirstNode(TimeSinceStartNode):
    pass


class SecondNode(TimeSinceStartNode):
    pass


class BasicSequentialWorkflow(BaseWorkflow):
    graph = StartNode >> FirstNode >> SecondNode

    class Outputs(BaseWorkflow.Outputs):
        first_node_time: int = FirstNode.Outputs.total_time
        second_node_time: int = SecondNode.Outputs.total_time


workflow = BasicSequentialWorkflow()
final_event = workflow.run()

assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.first_node_time == 1
assert final_event.outputs.second_node_time == 2


# nodes/time_since_beginning_node.py
class TimeSinceStartNode(BaseNode):
    start_time = StartNode.Outputs.start_time

    class Outputs(BaseNode.Outputs):
        total_time: int

    def run(self) -> Outputs:
        time.sleep(1)
        return self.Outputs(total_time=math.floor(time.time() - self.start_time))


# nodes/start_node.py
class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        start_time = time.time()


# --------------------------------------------------------
# State
# --------------------------------------------------------
print("\nState:")
print("---------------------------")
print("In most cases it’s sufficient to drive a Node’s behavior based on either inputs to the Workflow, or the outputs of upstream Nodes.")
print("However, Workflow’s also support writing to and reading from a global state object that lives for the duration of the Workflow’s execution.")
print("Here’s an example of how to define the schema of a State object and use it in a Workflow.")
print("---------------------------\n")

# Here’s an example of how to define the schema of a State object and use it in a Workflow.


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


workflow = MyWorkflow()
final_event = workflow.run()
assert final_event.name == "workflow.execution.fulfilled"
assert final_event.outputs.result == 2

print("Even if no State class is explicitly defined, Workflows use State under the hood to track all information about a Workflow’s execution.")
print("This information is stored under the reserved meta attribute on the State class and can be accessed for your own purposes.")
print("---------------------------\n")

# --------------------------------------------------------
# Streaming Outputs
# --------------------------------------------------------
print("\nStreaming Outputs:")
print("---------------------------")
print("Until now, we’ve only seen the run() method being invoked on Workflows we’ve defined.    run() is a blocking call that waits for the Workflow to complete before returning a terminal fulfilled or rejected event.")
print("In some cases, you may want to stream the events a Workflow produces as they’re being emitted.")
print("This is useful when your Workflow produces outputs along the way, and you want to consume them in real-time.")
print("You can do this via the stream() method, which returns a Generator that yields events as they’re produced.")
print("---------------------------\n")


class Inputs(BaseInputs):
    boost: int


class StartNode(BaseNode):
    boost = Inputs.boost

    class Outputs(BaseNode.Outputs):
        score: int

    def run(self) -> Outputs:
        return self.Outputs(score=random.randint(0, 10) + self.boost)


class EndNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        winner = StartNode.Outputs.score.greater_than(15)


class MyWorkflow(BaseWorkflow):
    graph = StartNode >> EndNode

    class Outputs(BaseWorkflow.Outputs):
        score = StartNode.Outputs.score
        winner = EndNode.Outputs.winner


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

print("---------------------------\n")

# --------------------------------------------------------
# Node Event Streaming
# --------------------------------------------------------
print("\nNode Event Streaming:")
print("---------------------------")
print("By default, when you call a Workflow’s stream() method, you’ll only receive Workflow-level events.")
print("However, you may also opt in to receive Node-level events by specifying the event_types parameter.")
print("With this, you can receive the events that Nodes in the Workflow produce as they’re emitted.")
print("This is useful when you want to inspect the outputs of individual Nodes for debugging purposes.")
print("---------------------------\n")


class Inputs(BaseInputs):
    boost: int


class StartNode(BaseNode):
    boost = Inputs.boost

    class Outputs(BaseNode.Outputs):
        score: int

    def run(self) -> Outputs:
        return self.Outputs(score=random.randint(0, 10) + self.boost)


class EndNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        winner = StartNode.Outputs.score.greater_than(15)


class MyWorkflow(BaseWorkflow):
    graph = StartNode >> EndNode

    class Outputs(BaseWorkflow.Outputs):
        winner = EndNode.Outputs.winner


workflow = MyWorkflow()
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

Was this page helpful?

Yes

No

# --------------------------------------------------------
# Summary
# --------------------------------------------------------
print("\nQuickstart Complete!")
print("You've learned about:")
print("1. Basic nodes and workflows")
print("2. Node outputs")
print("3. Workflow inputs")
print("4. Control flow")
print("5. Parallel execution")
print("6. State management")
print("---------------------------\n")
