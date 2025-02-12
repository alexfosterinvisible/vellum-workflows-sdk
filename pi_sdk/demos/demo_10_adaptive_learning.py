"""Demo 10: Adaptive Learning Analysis.

This demo shows:
1. Testing different adaptive learning approaches
2. Analyzing response-based adjustments
3. Optimizing learning pathways
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
    "name": "Math Adaptive Learning",
    "description": """Evaluate mathematical explanations with a focus on adaptation.
    Test various adaptive learning strategies to identify the most effective
    approaches for personalizing instruction based on responses."""
}

TEST_CASES = [
    {
        "style": "Progressive Difficulty",
        "input": "Teach factoring quadratic expressions with adaptive difficulty.",
        "output": """Let's learn factoring with adjusting difficulty! 📈

Level 1: Basic Recognition
-------------------------
Start with simple perfect squares:
x² + 2x + 1

🤔 What do you notice?
* Square of first term: x²
* Middle term: 2x
* Last term: 1

✅ This is (x + 1)²!

If this is clear, let's advance...
If not, let's practice more squares.

Level 2: Simple Factoring
------------------------
Try this one:
x² + 5x + 6

Strategy:
1. Find factors of 6: 1, 2, 3, 6
2. Which pair adds to 5?
   * 2 + 3 = 5 ✓

Therefore: (x + 2)(x + 3)

Need more practice here?
* If yes: Try x² + 7x + 12
* If no: Move to Level 3

Level 3: Challenging Cases
------------------------
Ready for this:
2x² + 7x + 3

Advanced strategy:
1. Multiply a: 2x² → need ac = 6
2. Find factors of 6 that add to b (7):
   * 6 + 1 = 7 ✓
3. Rewrite middle term:
   2x² + 6x + x + 3
4. Group terms:
   2x(x + 3) + 1(x + 3)
   (2x + 1)(x + 3)

💡 Adaptive Pathways:
* Struggling? → Return to Level 2
* Confident? → Try harder problems
* Just right? → Practice more here

Level 4: Expert Challenge
-----------------------
If ready, try:
3x² - 7x - 6

Master strategy:
1. a = 3, c = -6
2. Need factors of -18 adding to -7
3. -9 + 2 = -7
4. Rewrite and group...

🎯 Choose Your Path:
1. Need review? Go back to:
   * Perfect squares
   * Simple factoring
   * Grouping method

2. Ready for more? Try:
   * Larger coefficients
   * Special patterns
   * Complex grouping

3. Want practice? Use:
   * Similar difficulty
   * Mixed problems
   * Timed challenges

✨ Adaptive Features:
1. Multiple entry points
2. Flexible progression
3. Review options
4. Challenge paths
5. Self-paced learning

📊 Progress Tracking:
* Master each level
* Build confidence
* Identify patterns
* Apply strategies

🔄 Adjustment Points:
* After each problem
* Between levels
* Based on confidence
* Following errors

Remember:
* Take your time
* Build strong foundations
* Ask for help when needed
* Celebrate progress

Next Steps:
Choose your path:
1. More practice at current level
2. Move up in difficulty
3. Quick review of basics
4. Challenge yourself"""
    },
    {
        "style": "Conceptual Branching",
        "input": "Explain solving word problems with adaptive conceptual focus.",
        "output": """Let's explore word problems with flexible understanding! 🌳

Core Concept: Problem Solving
---------------------------
Start here:
"A store sells notebooks for $3 each. How much for 5 notebooks?"

🤔 Understanding Check:
Do you see this as:
A) Repeated addition
B) Multiplication
C) Not sure

Path A: Addition Focus
--------------------
Think: $3 + $3 + $3 + $3 + $3
* Count by 3s
* Track the total
* Verify the count

✅ If this helps, try more addition.
❓ If too simple, try Path B.

Path B: Multiplication View
-------------------------
Think: 5 × $3
* Groups of equal size
* Quick calculation
* Pattern recognition

✅ If this clicks, try harder problems.
❓ If unclear, return to Path A.

Branching Problem:
"A store has 24 notebooks. They're sold in packs of 4.
How many packs can they make?"

Choose Your Approach:
1. Division as repeated subtraction
   * Start with 24
   * Subtract 4 until zero
   * Count subtractions

2. Division as grouping
   * Make groups of 4
   * Count complete groups
   * Check remaining items

3. Division as inverse
   * 4 × ? = 24
   * Find missing factor
   * Verify answer

🔄 Adaptive Elements:
* Choose your path
* Switch methods
* Combine approaches
* Build connections

Challenge Selection:
------------------
Based on understanding:

Basic:
"15 candies shared by 3 friends"
* If clear → advance
* If unsure → practice more
* If confused → review basics

Intermediate:
"72 cookies packed in boxes of 8"
* If confident → continue
* If hesitant → more practice
* If struggling → step back

Advanced:
"A baker sells cookies for $2 each.
In one day, she makes $54.
How many cookies did she sell?"
* Multiple steps
* Inverse operations
* Real context

💡 Learning Pathways:
1. Visual → Numerical
2. Concrete → Abstract
3. Simple → Complex
4. Direct → Inverse

📊 Progress Markers:
* Understanding concepts
* Solving independently
* Explaining methods
* Choosing strategies

🎯 Adjustment Triggers:
* Correct solutions
* Error patterns
* Solution methods
* Explanation quality

Next Steps Options:
1. More similar problems
2. Increased complexity
3. Different contexts
4. Mixed practice

Remember:
* Multiple approaches work
* Build understanding
* Make connections
* Practice regularly"""
    },
    {
        "style": "Error-Based Adaptation",
        "input": "Guide through common algebra mistakes with adaptive correction.",
        "output": """Let's learn from mistakes and adapt our approach! 🔍

Starting Point: Solve 2x + 3 = 7
-------------------------------
Common Error 1:
2x + 3 = 7
2x = 7 + 3
2x = 10
x = 5 ❌

🚫 Error Detected:
* Added instead of subtracted
* Moved term to wrong side

✅ Correction Path A:
Think: "Move terms by doing opposite"
2x + 3 = 7
2x = 7 - 3
2x = 4
x = 2

If this error occurs:
* Practice more subtraction
* Review opposite operations
* Try similar problems

Common Error 2:
2x = 4
x = 4 × 2
x = 8 ❌

🚫 Error Detected:
* Multiplied instead of divided
* Confused inverse operation

✅ Correction Path B:
Think: "Divide both sides by 2"
2x = 4
x = 4 ÷ 2
x = 2

If this error occurs:
* Practice division
* Review equation balance
* Try more examples

Adaptive Practice Based on Errors:
--------------------------------
Error Type 1: Sign Errors
------------------------
Problem: 3x - 4 = 8

Common mistake:
3x = 8 - (-4) ❌

Correction paths:
1. Number line practice
2. Opposite operation rules
3. Step-by-step checking

Error Type 2: Distribution
-------------------------
Problem: 2(x + 3) = 10

Common mistake:
2x + 3 = 10 ❌

Correction paths:
1. Area model practice
2. Term-by-term multiplication
3. Verification methods

Error Type 3: Fractions
----------------------
Problem: (x + 2)/3 = 4

Common mistake:
x + 2 = 4/3 ❌

Correction paths:
1. Fraction multiplication
2. Equation balance
3. Check solutions

🔄 Adaptive Responses:
1. For Sign Errors:
   * Use number lines
   * Practice with negatives
   * Check each step

2. For Distribution:
   * Draw diagrams
   * Expand step by step
   * Verify expansion

3. For Fractions:
   * Review multiplication
   * Practice with simple numbers
   * Check reasonableness

📊 Error Tracking:
* Note common mistakes
* Identify patterns
* Target practice
* Build confidence

�� Practice Selection:
Based on errors:
1. Similar problems
2. Simplified versions
3. Step-by-step practice
4. Mixed review

💡 Learning Strategies:
* Understand why errors occur
* Practice correct methods
* Verify solutions
* Build checking habits

Next Steps:
Choose based on errors:
1. More basic practice
2. Similar problems
3. Advanced challenges
4. Mixed review

Remember:
* Mistakes help learning
* Take time to understand
* Practice corrections
* Build confidence"""
    },
    {
        "style": "Skill-Based Progression",
        "input": "Teach solving equations with adaptive skill development.",
        "output": """Let's build equation-solving skills progressively! 📈

Skill Level 1: Basics
--------------------
Core Skills:
* Adding/subtracting
* Order of operations
* Number properties

Starting Problem:
x + 5 = 12

✅ Mastery Check:
* Can you isolate x?
* Do you understand why?
* Ready for more?

Progress Options:
1. More practice here
2. Add difficulty
3. Review basics

Skill Level 2: Two Steps
-----------------------
New Skills:
* Multiple operations
* Strategy planning
* Solution checking

Problem: 2x + 3 = 11

🔍 Skill Assessment:
1. Can you:
   * Plan steps
   * Execute correctly
   * Verify answer

2. Choose path:
   * Need practice? → More similar
   * Confident? → Level 3
   * Struggling? → Review Level 1

Skill Level 3: Variables Both Sides
---------------------------------
Advanced Skills:
* Term collection
* Strategic moves
* Efficiency

Problem: 3x + 2 = x + 10

💪 Skill Building:
1. Collect like terms
2. Isolate variable
3. Solve and check

Adaptation Points:
* After each solution
* Between skill levels
* Based on accuracy
* Following errors

Skill Level 4: Complex Equations
------------------------------
Master Skills:
* Distribution
* Fraction operations
* Multi-step planning

Problem: 2(x + 3) = 3(x - 1)

🎯 Skill Integration:
* Use all previous skills
* Plan solution path
* Execute efficiently
* Verify result

📊 Skill Tracking:
Basic Skills:
* Number operations ✓
* Term movement ✓
* Solution steps ✓

Intermediate Skills:
* Term collection
* Strategy selection
* Verification methods

Advanced Skills:
* Distribution
* Fraction operations
* Complex planning

🔄 Progression Paths:
1. Linear Path:
   * Master each level
   * Build on basics
   * Regular practice

2. Branching Path:
   * Focus on needs
   * Extra practice
   * Skill building

3. Challenge Path:
   * Skip basics
   * Advanced problems
   * Complex skills

💡 Adaptive Features:
* Skill-based advancement
* Flexible progression
* Targeted practice
* Regular assessment

Practice Selection:
-----------------
Based on skills:
1. Basic:
   * One-step equations
   * Number properties
   * Simple operations

2. Intermediate:
   * Two-step equations
   * Like terms
   * Basic distribution

3. Advanced:
   * Complex equations
   * Fraction operations
   * Multiple steps

🎯 Mastery Checks:
At each level:
* Solve independently
* Explain process
* Apply to new problems
* Help others

Next Steps:
Choose path based on:
1. Current skill level
2. Confidence
3. Error patterns
4. Learning goals

Remember:
* Build strong foundations
* Practice regularly
* Track progress
* Celebrate success"""
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
logger = logging.getLogger("demo_10")


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


def analyze_adaptation(results: List[Dict]) -> Dict:
    """Analyze effectiveness of adaptive learning patterns."""
    analysis = {
        "overall_scores": {},
        "adaptation_elements": {},
        "element_effectiveness": {},
        "recommendations": []
    }

    # Track adaptation elements
    element_scores = {
        "progression": [],
        "branching": [],
        "error_handling": [],
        "skill_building": [],
        "assessment": []
    }

    for result in results:
        style = result["style"]
        scores = result["scores"]
        output = result["output"].lower()

        # Overall scores
        analysis["overall_scores"][style] = scores["total_score"]

        # Track elements used
        elements_used = []
        if "level" in output or "progress" in output or "advance" in output:
            elements_used.append("progression")
            element_scores["progression"].append(scores["total_score"])
        if "path" in output or "choose" in output or "option" in output:
            elements_used.append("branching")
            element_scores["branching"].append(scores["total_score"])
        if "error" in output or "mistake" in output or "correct" in output:
            elements_used.append("error_handling")
            element_scores["error_handling"].append(scores["total_score"])
        if "skill" in output or "master" in output or "practice" in output:
            elements_used.append("skill_building")
            element_scores["skill_building"].append(scores["total_score"])
        if "check" in output or "assess" in output or "verify" in output:
            elements_used.append("assessment")
            element_scores["assessment"].append(scores["total_score"])

        analysis["adaptation_elements"][style] = elements_used

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
        "Combine multiple adaptation methods",
        "Start with clear progression paths",
        "Include regular skill assessment",
        "Provide error-specific practice"
    ])

    return analysis


def display_results(results: List[Dict], analysis: Dict):
    """Display results and analysis."""
    # Scores table
    scores_table = Table(title="Adaptive Learning Analysis")
    scores_table.add_column("Style", style="cyan")
    scores_table.add_column("Total Score", style="green")
    scores_table.add_column("Elements Used", style="yellow")

    for result in results:
        style = result["style"]
        elements = analysis["adaptation_elements"][style]
        scores_table.add_row(
            style,
            f"{analysis['overall_scores'][style]:.2f}",
            "\n".join(elements)
        )

    # Elements table
    elements_table = Table(title="Adaptation Element Effectiveness")
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
    output_file = OUTPUT_DIR / "demo_10_results.json"

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
            console.print("\n[bold]Testing Adaptive Learning[/bold]")
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
                analysis = analyze_adaptation(scored_cases)
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
    console.print("\n[bold]Running Demo 10: Adaptive Learning Analysis[/bold]")
    asyncio.run(main())
