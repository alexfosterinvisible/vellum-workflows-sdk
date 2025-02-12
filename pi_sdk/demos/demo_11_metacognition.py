"""Demo 11: Metacognitive Strategies Analysis.

This demo shows:
1. Testing different metacognitive approaches
2. Analyzing self-reflection patterns
3. Optimizing learning awareness
v1 - Initial implementation
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import aiohttp
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

# Configuration
API_KEY = "pilabs_key_epc8PlKUV7BzrsVJUJRzE3h3XLgxXa2zC6Hh7RSkIEo"
BASE_URL = "https://api.withpi.ai/v1"
OUTPUT_DIR = Path("demo_results")

# Test data
MATH_CONTRACT = {
    "name": "Math Metacognition",
    "description": """Evaluate mathematical explanations with a focus on metacognition.
    Test various metacognitive strategies to identify the most effective
    approaches for promoting self-awareness and learning regulation."""
}

TEST_CASES = [
    {
        "style": "Self-Questioning",
        "input": "Guide students through understanding limits in calculus using metacognitive strategies.",
        "output": """Let's explore limits through thoughtful self-questioning! 🤔

Understanding Check
-----------------
Before we start, ask yourself:
* What do I know about limits?
* Where have I seen them before?
* What makes them challenging?

Take a moment to write your thoughts...

Core Concept: Limit Approach
--------------------------
Consider: lim(x→2) (x² - 4)/(x - 2)

🤔 Self-Questions:
1. What am I seeing?
   * A fraction
   * x approaching 2
   * Similar terms

2. What happens if I try x = 2?
   * Numerator: 2² - 4 = 0
   * Denominator: 2 - 2 = 0
   * Result: 0/0 (undefined!)

3. Why did this happen?
   * Both parts equal zero
   * Division by zero undefined
   * Need another approach

Strategy Development
------------------
Ask yourself:
* Can I factor the numerator?
* What patterns do I notice?
* Is there a simpler way?

💭 Reflection Point:
"The numerator factors to (x+2)(x-2)
The denominator is (x-2)
I see a common factor!"

Solution Path
-----------
Think through:
1. Why can I cancel (x-2)?
2. What happens after canceling?
3. Where could this go wrong?

Result: lim(x→2) (x+2) = 4

Understanding Deepening
--------------------
Question your process:
* Why did this work?
* What principles did I use?
* Where else could this help?

🔍 Learning Check:
Can you explain:
* The initial problem?
* Your solution strategy?
* Why the answer makes sense?

Pattern Recognition
-----------------
Reflect on similar problems:
* When do we get 0/0?
* What strategies help?
* How do we verify limits?

📝 Learning Journal:
Record your insights:
1. What was new today?
2. What connections did you make?
3. What questions remain?

Problem Extension
---------------
Challenge yourself:
* What if x approaches other values?
* What about different functions?
* How do graphs help?

🤔 Metacognitive Prompts:
* How did you approach this?
* What strategies worked best?
* Where did you get stuck?
* How did you overcome challenges?

Strategy Review
-------------
Evaluate your methods:
* What worked well?
* What needed improvement?
* What will you try next time?

💡 Learning Insights:
1. Process awareness
2. Strategy selection
3. Error recognition
4. Solution verification

Next Steps
---------
Plan your learning:
1. What to practice?
2. Which concepts to review?
3. When to seek help?
4. How to apply this?

Remember:
* Question your thinking
* Monitor understanding
* Adjust strategies
* Reflect regularly"""
    },
    {
        "style": "Strategy Monitoring",
        "input": "Help students solve optimization problems with metacognitive monitoring.",
        "output": """Let's solve optimization with strategic awareness! 📊

Strategy Planning Phase
--------------------
Problem: Find the maximum area of a rectangle with perimeter 20 units.

🤔 Pre-Solution Questions:
1. What do I know?
   * Perimeter = 20
   * Need to find area
   * Looking for maximum

2. What strategies could work?
   * Algebra
   * Calculus
   * Graphing

3. How will I choose?
   * Consider complexity
   * Check prerequisites
   * Evaluate efficiency

Strategy Selection
----------------
Monitor your thinking:
* Why choose calculus?
* What makes it suitable?
* How confident are you?

✍️ Strategy Documentation:
"I'll use calculus because:
* Area is a function
* Need to find maximum
* Have derivative tools"

Implementation Monitoring
----------------------
Step 1: Set up equation
* Let width = x
* Length = (20-2x)/2
* Area = x(10-x)

🔍 Check Understanding:
* Why did we use 20-2x?
* How does this represent area?
* What are the constraints?

Step 2: Find derivative
A = x(10-x) = 10x - x²
A' = 10 - 2x

💭 Strategy Check:
* Why take derivative?
* What does A' tell us?
* How find maximum?

Step 3: Solve A' = 0
10 - 2x = 0
x = 5

📊 Progress Monitor:
* Does this make sense?
* What does x=5 mean?
* Need to verify?

Solution Verification
------------------
Check your work:
1. Dimensions:
   * Width = 5
   * Length = 5
   * Perimeter = 20 ✓

2. Area = 25 square units

🤔 Verification Questions:
* Is this reasonable?
* How can we prove it's maximum?
* What about other points?

Strategy Evaluation
-----------------
Assess your approach:
* What worked well?
* Where did you pause?
* What would you change?

💡 Method Insights:
1. Setting up equations
2. Using derivatives
3. Verifying solutions
4. Interpreting results

Learning Transfer
---------------
Think ahead:
* Where else use this?
* What patterns help?
* How adapt method?

📝 Strategy Journal:
Record key points:
1. Problem approach
2. Decision points
3. Verification steps
4. Learning insights

Metacognitive Review
------------------
Reflect on process:
* Strategy selection
* Implementation
* Verification
* Understanding

🎯 Strategy Refinement:
* What to keep?
* What to modify?
* What to add?
* What to remove?

Future Applications
----------------
Plan ahead:
1. Similar problems
2. Different contexts
3. Strategy adaptations
4. Learning needs

Remember:
* Monitor your thinking
* Check understanding
* Verify solutions
* Reflect on process"""
    },
    {
        "style": "Learning Reflection",
        "input": "Guide students through understanding probability with reflective learning.",
        "output": """Let's explore probability through deep reflection! 🎲

Initial Knowledge Check
--------------------
Reflect on your understanding:
1. What is probability?
2. Where do you see it?
3. Why is it useful?

📝 Knowledge Inventory:
* What's clear?
* What's fuzzy?
* What's missing?

Core Concept: Probability Basics
-----------------------------
Example: Rolling a die

🤔 Reflection Points:
1. Before rolling:
   * What might happen?
   * How many outcomes?
   * What's most likely?

2. After understanding:
   * Why six outcomes?
   * How calculate chances?
   * What patterns emerge?

Learning Process
--------------
Monitor your thinking:
* How do you view probability?
* What makes it click?
* Where do you struggle?

💭 Understanding Check:
"I see probability as:
* Measuring chance
* Predicting outcomes
* Using fractions"

Concept Application
-----------------
Problem: Two dice roll

Self-Questions:
1. Planning:
   * How approach this?
   * What tools needed?
   * Where to start?

2. Implementation:
   * Why multiply outcomes?
   * How list possibilities?
   * What patterns help?

3. Verification:
   * Does answer make sense?
   * How can I check?
   * What might I miss?

🔍 Learning Insights:
* Connections made
* Strategies used
* Challenges faced
* Solutions found

Understanding Deepening
--------------------
Reflect on growth:
1. Initial thoughts:
   * Simple counting
   * Basic fractions
   * Single events

2. New understanding:
   * Multiple events
   * Compound probability
   * Systematic counting

3. Future applications:
   * Real-world uses
   * Problem-solving
   * Decision making

📊 Learning Progress:
Track your growth:
* What's improved?
* What's clearer now?
* What needs work?

Concept Integration
----------------
Connect ideas:
* Probability and fractions
* Chance and statistics
* Theory and practice

🌟 Knowledge Building:
1. Foundation:
   * Basic concepts
   * Simple problems
   * Clear examples

2. Development:
   * Complex problems
   * Multiple approaches
   * Deep understanding

3. Application:
   * Real situations
   * Problem-solving
   * Decision making

Reflection Strategies
------------------
Review your methods:
* What helped most?
* Which examples worked?
* How organize thinking?

💡 Learning Tools:
1. Visual aids
2. Practice problems
3. Real examples
4. Self-questioning

Progress Assessment
-----------------
Check understanding:
* Concept clarity
* Problem-solving
* Application ability
* Confidence level

🎯 Next Steps:
Plan your learning:
1. Review needs
2. Practice areas
3. Application goals
4. Understanding gaps

Remember:
* Reflect regularly
* Question deeply
* Connect ideas
* Apply learning"""
    },
    {
        "style": "Understanding Analysis",
        "input": "Help students analyze their understanding of algebraic proofs.",
        "output": """Let's analyze our understanding of algebraic proofs! 🔍

Knowledge Analysis
---------------
Examine your understanding:

1. Current Knowledge:
   □ What is a proof?
   □ Why use algebra?
   □ How structure proofs?

2. Knowledge Gaps:
   □ Unclear concepts
   □ Missing connections
   □ Needed skills

🤔 Understanding Map:
* Strong areas
* Weak points
* Learning needs

Proof Analysis Example
-------------------
Prove: (a + b)² = a² + 2ab + b²

Self-Analysis Questions:
1. Before Starting:
   * What do I know about squares?
   * How expand expressions?
   * Why this pattern matters?

2. During Proof:
   * Why each step?
   * What rules apply?
   * How verify work?

3. After Completion:
   * What did I learn?
   * Where was I stuck?
   * What helped most?

💭 Understanding Check:
Monitor your thinking:
* Logic flow
* Step connections
* Pattern recognition

Proof Development
---------------
Track your process:
1. Initial approach:
   * Expand directly
   * Use FOIL
   * Check terms

2. Strategy analysis:
   * Why this method?
   * What alternatives?
   * How efficient?

3. Verification:
   * All terms included?
   * Steps logical?
   * Result valid?

📊 Progress Tracking:
Document your learning:
* New insights
* Clear concepts
* Remaining questions

Understanding Layers
-----------------
Analyze depth:
1. Surface level:
   * Basic steps
   * Simple rules
   * Direct application

2. Deep understanding:
   * Connections
   * Patterns
   * Applications

3. Mastery level:
   * Create proofs
   * Explain clearly
   * Apply widely

🔍 Concept Analysis:
Break down learning:
* Key components
* Critical steps
* Essential patterns

Learning Assessment
----------------
Evaluate understanding:
1. Can you:
   * Explain the proof?
   * Create similar ones?
   * Spot patterns?

2. Do you understand:
   * Why it works?
   * Where it applies?
   * How to extend it?

💡 Understanding Growth:
Track development:
* Initial state
* Current level
* Next steps

Application Analysis
-----------------
Study your use:
1. Where apply this?
   * Similar problems
   * Different contexts
   * Real situations

2. How adapt method?
   * New problems
   * Different patterns
   * Complex cases

🎯 Learning Direction:
Plan development:
* Skills to build
* Concepts to master
* Applications to try

Understanding Blocks
-----------------
Analyze challenges:
* What's unclear?
* Why difficult?
* How overcome?

📝 Learning Journal:
Record insights:
1. Key learnings
2. Helpful strategies
3. Future needs
4. Growth areas

Remember:
* Analyze deeply
* Track progress
* Question understanding
* Apply learning"""
    }
]

# Logging setup
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("demo_11")


async def generate_dimensions(session: aiohttp.ClientSession, contract: Dict) -> Optional[Dict]:
    """Generate dimensions for a contract."""
    try:
        async with session.post(
            f"{BASE_URL}/contracts/generate_dimensions",
            json={"contract": contract}
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error(f"Failed to generate dimensions: {await resp.text()}")
                return None
    except Exception as e:
        logger.error(f"Error generating dimensions: {e}")
        return None


async def score_response(
    session: aiohttp.ClientSession,
    contract: Dict,
    test_case: Dict
) -> Optional[Dict]:
    """Score a test response."""
    try:
        async with session.post(
            f"{BASE_URL}/contracts/score",
            json={
                "contract": contract,
                "llm_input": test_case["input"],
                "llm_output": test_case["output"]
            }
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error(f"Failed to score response: {await resp.text()}")
                return None
    except Exception as e:
        logger.error(f"Error scoring response: {e}")
        return None


def analyze_metacognition(results: List[Dict]) -> Dict:
    """Analyze effectiveness of metacognitive strategies."""
    analysis = {
        "overall_scores": {},
        "metacognitive_elements": {},
        "element_effectiveness": {},
        "recommendations": []
    }

    # Track metacognitive elements
    element_scores = {
        "self_questioning": [],
        "monitoring": [],
        "reflection": [],
        "analysis": [],
        "planning": []
    }

    for result in results:
        style = result["style"]
        scores = result["scores"]
        output = result["output"].lower()

        # Overall scores
        analysis["overall_scores"][style] = scores["total_score"]

        # Track elements used
        elements_used = []
        if "question" in output or "ask" in output or "why" in output:
            elements_used.append("self_questioning")
            element_scores["self_questioning"].append(scores["total_score"])
        if "monitor" in output or "check" in output or "track" in output:
            elements_used.append("monitoring")
            element_scores["monitoring"].append(scores["total_score"])
        if "reflect" in output or "think" in output or "consider" in output:
            elements_used.append("reflection")
            element_scores["reflection"].append(scores["total_score"])
        if "analyze" in output or "examine" in output or "study" in output:
            elements_used.append("analysis")
            element_scores["analysis"].append(scores["total_score"])
        if "plan" in output or "strategy" in output or "approach" in output:
            elements_used.append("planning")
            element_scores["planning"].append(scores["total_score"])

        analysis["metacognitive_elements"][style] = elements_used

    # Analyze element effectiveness
    for element, scores in element_scores.items():
        if scores:
            analysis["element_effectiveness"][element] = sum(scores) / len(scores)

    # Generate recommendations
    sorted_elements = sorted(
        analysis["element_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    analysis["recommendations"].extend([
        f"Most effective element: {sorted_elements[0][0]} ({sorted_elements[0][1]:.2f})",
        "Combine multiple metacognitive strategies",
        "Start with self-questioning",
        "Include regular monitoring",
        "End with reflection and analysis"
    ])

    return analysis


def display_results(results: List[Dict], analysis: Dict):
    """Display results and analysis."""
    # Scores table
    scores_table = Table(title="Metacognitive Strategies Analysis")
    scores_table.add_column("Style", style="cyan")
    scores_table.add_column("Total Score", style="green")
    scores_table.add_column("Elements Used", style="yellow")

    for result in results:
        style = result["style"]
        elements = analysis["metacognitive_elements"][style]
        scores_table.add_row(
            style,
            f"{analysis['overall_scores'][style]:.2f}",
            "\n".join(elements)
        )

    # Elements table
    elements_table = Table(title="Metacognitive Element Effectiveness")
    elements_table.add_column("Element", style="cyan")
    elements_table.add_column("Average Score", style="green")

    for element, score in sorted(
        analysis["element_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        elements_table.add_row(
            element.title(),
            f"{score:.2f}"
        )

    # Recommendations table
    recommendations_table = Table(title="Best Practices")
    recommendations_table.add_column("Category", style="cyan")
    recommendations_table.add_column("Details", style="yellow")

    recommendations_table.add_row(
        "Top Element",
        analysis["recommendations"][0]
    )
    recommendations_table.add_row(
        "Best Practices",
        "\n".join(analysis["recommendations"][1:])
    )

    # Display all tables
    console.print("\n")
    console.print(scores_table)
    console.print("\n")
    console.print(elements_table)
    console.print("\n")
    console.print(recommendations_table)


def save_results(results: Dict):
    """Save results to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "demo_11_results.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Results saved to {output_file}")


async def main():
    """Run the demo."""
    results = {
        "contract": MATH_CONTRACT,
        "test_cases": [],
        "success": False
    }

    # Create session with auth
    async with aiohttp.ClientSession(headers={
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }) as session:
        # Generate dimensions
        console.print("\n[bold]Generating Contract Dimensions[/bold]")
        if contract_with_dims := await generate_dimensions(session, MATH_CONTRACT):
            results["dimensions"] = contract_with_dims.get("dimensions", [])
            console.print("[green]✓ Generated dimensions[/green]")

            # Test each case
            console.print("\n[bold]Testing Metacognitive Strategies[/bold]")
            scored_cases = []
            for case in TEST_CASES:
                if scores := await score_response(session, contract_with_dims, case):
                    scored_case = {
                        "style": case["style"],
                        "input": case["input"],
                        "output": case["output"],
                        "scores": scores
                    }
                    results["test_cases"].append(scored_case)
                    scored_cases.append(scored_case)
                    console.print(f"[green]✓ Scored {case['style']}[/green]")

            # Analyze and display results
            if scored_cases:
                analysis = analyze_metacognition(scored_cases)
                results["analysis"] = analysis

                console.print("\n[bold]Analysis Results[/bold]")
                display_results(scored_cases, analysis)
                results["success"] = True

        # Save results
        save_results(results)

        if results["success"]:
            console.print("\n[bold green]Demo completed successfully![/bold green]")
        else:
            console.print("\n[bold red]Demo failed![/bold red]")


if __name__ == "__main__":
    console.print("\n[bold]Running Demo 11: Metacognitive Strategies Analysis[/bold]")
    asyncio.run(main())
