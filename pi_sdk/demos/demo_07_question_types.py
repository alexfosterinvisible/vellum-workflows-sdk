"""Demo 7: Question Types Analysis.

This demo shows:
1. Testing different question patterns
2. Analyzing effectiveness of question types
3. Optimizing question strategies
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
    "name": "Math Question Patterns",
    "description": """Evaluate mathematical explanations with a focus on question types.
    Test various questioning strategies to identify the most effective
    approaches for promoting understanding and engagement."""
}

TEST_CASES = [
    {
        "style": "Socratic Questioning",
        "input": "Explain why a negative number times a negative number equals a positive number.",
        "output": """Let's explore this concept through guided questions! 🤔

1. Understanding Patterns
------------------------
Q: What happens when we multiply a positive by a positive?
A: We get a positive! (e.g., 2 × 3 = 6)

Q: What happens when we multiply a positive by a negative?
A: We get a negative! (e.g., 2 × -3 = -6)

Q: Can you predict what happens with negative × negative?
[Think about the pattern...]

2. Real-world Connection
-----------------------
Q: If going north is positive, what represents going south?
A: Going south would be negative direction.

Q: If you reverse a negative direction, what happens?
A: You end up going in the positive direction!

3. Mathematical Logic
--------------------
Consider this sequence:
* 3 × 2 = 6
* 3 × 1 = 3
* 3 × 0 = 0
* 3 × -1 = -3
* 3 × -2 = -6

Q: What pattern do you notice?
A: Each product decreases by 3.

Now look at this:
* -3 × 2 = -6
* -3 × 1 = -3
* -3 × 0 = 0
* -3 × -1 = 3
* -3 × -2 = 6

Q: What changed in the pattern?
A: The products increase by 3!

4. Understanding Why
-------------------
Q: When we multiply by a negative number, what happens to the pattern?
A: The pattern reverses direction!

Q: So when we multiply two negatives, what happens?
A: We reverse direction twice, ending up positive!

5. Final Verification
--------------------
Q: Can you explain why (-2) × (-3) = 6?
A: When we multiply by -2, we reverse -3 to get 3,
   then multiply by 2 to get 6!

💡 Key Insight:
Multiplying by a negative means "reverse and take that many steps."
Two reversals bring us back to the positive direction!

Want to explore more?
1. What happens with three negative numbers?
2. How does this relate to dividing negative numbers?
3. Can you create your own explanation using this pattern?"""
    },
    {
        "style": "Diagnostic Questions",
        "input": "Explain how to solve quadratic equations using the quadratic formula: ax² + bx + c = 0",
        "output": """Let's master the quadratic formula through targeted questions! 📝

Pre-Assessment Questions:
------------------------
1. What type of equation is ax² + bx + c = 0?
   □ Linear
   □ Quadratic
   □ Cubic
   [Answer: Quadratic - it has x²]

2. Can you identify a, b, and c in: x² - 5x + 6 = 0?
   a = ___  b = ___  c = ___
   [Answer: a = 1, b = -5, c = 6]

Understanding the Formula:
-------------------------
The quadratic formula is: x = [-b ± √(b² - 4ac)] ÷ (2a)

Q: Why do we need ± in the formula?
A: Because a quadratic equation usually has two solutions!

Concept Check Questions:
-----------------------
1. What do we call b² - 4ac?
   □ Quadratic term
   □ Discriminant
   □ Coefficient
   [Answer: Discriminant]

2. What does the discriminant tell us?
   □ Number of solutions
   □ Size of solutions
   □ Sign of solutions
   [Answer: Number of solutions]

Practice Application:
-------------------
Let's solve: x² - 5x + 6 = 0

Step-by-Step Questions:
1. What are a, b, and c?
   a = 1, b = -5, c = 6

2. What's the discriminant (b² - 4ac)?
   (-5)² - 4(1)(6) = 25 - 24 = 1

3. What's -b ± √(discriminant)?
   5 ± √1 = 5 ± 1

4. What's the final answer?
   x = (5 ± 1) ÷ 2
   x = 3 or x = 2

Verification Questions:
---------------------
1. Check x = 3:
   3² - 5(3) + 6 = 9 - 15 + 6 = 0 ✓

2. Check x = 2:
   2² - 5(2) + 6 = 4 - 10 + 6 = 0 ✓

Understanding Check:
------------------
Q: What happens if b² - 4ac is:
1. Positive? [Two real solutions]
2. Zero? [One real solution]
3. Negative? [No real solutions]

🎯 Quick Quiz:
1. In x² + 2x + 1 = 0:
   * What's the discriminant?
   * How many solutions?
   * What are they?
   [Try it yourself!]

Want to practice more?
1. What's the discriminant of x² + x + 1 = 0?
2. When does a quadratic have exactly one solution?
3. Can you create your own quadratic with two solutions?"""
    },
    {
        "style": "Scaffolded Questions",
        "input": "Explain how to find the area of a circle given its radius.",
        "output": """Let's build our understanding step by step with guiding questions! 🎯

Level 1: Basic Concepts
----------------------
Q: What's special about a circle?
A: Every point is the same distance from the center!

Q: What do we call this distance?
A: The radius (r)

Level 2: Understanding π
-----------------------
Q: What happens when we divide a circle's circumference by its diameter?
A: We always get π (approximately 3.14159)!

Q: Why is this important?
A: It shows a constant relationship in all circles!

Level 3: Building the Formula
----------------------------
Q: If we divide a circle into tiny triangles:
1. What's the height of each triangle? [radius]
2. What's the total width at the base? [circumference]
3. What's the formula for a triangle's area? [½ × base × height]

Let's connect the dots:
* Circumference = 2πr
* Each triangle: Area = ½ × base × r
* Total area combines all these triangles!

Q: Can you see how this leads to A = πr²?

Level 4: Understanding the Formula
--------------------------------
A = πr²

Q: What happens to the area when we:
1. Double the radius? [Area increases 4 times]
2. Triple the radius? [Area increases 9 times]
3. Halve the radius? [Area decreases to ¼]

Level 5: Application
-------------------
Let's find the area of a circle with radius 5 cm:
1. What's our formula? [A = πr²]
2. What do we plug in for r? [5]
3. What's 5²? [25]
4. So what's the area? [25π ≈ 78.54 cm²]

Level 6: Real-world Connection
----------------------------
Q: Why might we need to find a circle's area?
Examples:
* Pizza sizing
* Circular pool coverage
* Round table seating

Practice Questions:
-----------------
1. Basic: Find the area of a circle with radius 3 cm
2. Medium: How much does the area increase if radius goes from 2 to 4?
3. Challenge: If a circle's area is 100π, what's its radius?

💡 Understanding Check:
* Why do we square the radius?
* Why do we multiply by π?
* How does changing radius affect area?

Want to explore more?
1. How does this relate to the area of a sector?
2. What's the relationship between radius and circumference?
3. Can you explain why A = πr² to someone else?"""
    },
    {
        "style": "Challenge Questions",
        "input": "Explain the concept of probability using coin flips and dice rolls.",
        "output": """Let's explore probability through increasingly challenging questions! 🎲

Level 1: Basic Probability
-------------------------
🎯 Warm-up Challenge:
Q: When flipping a fair coin:
1. What's the probability of heads? [1/2]
2. What's the probability of tails? [1/2]
3. What do these probabilities sum to? [1]

✨ Key Concept:
Total probability of all possible outcomes = 1

Level 2: Multiple Events
-----------------------
🎯 Coin Flip Challenge:
Q: When flipping two coins:
1. List all possible outcomes:
   * HH
   * HT
   * TH
   * TT

2. What's the probability of:
   * Two heads? [1/4]
   * At least one head? [3/4]
   * No heads? [1/4]

🤔 Think Deeper:
Why is P(at least one head) = 3/4?
[Hint: Count favorable outcomes!]

Level 3: Dice Probability
------------------------
🎯 Single Die Challenge:
Q: Rolling one die:
1. How many possible outcomes? [6]
2. P(rolling a 6)? [1/6]
3. P(rolling an even number)? [3/6 = 1/2]

🎯 Advanced Challenge:
Rolling two dice:
1. How many total possibilities? [36]
2. P(sum = 7)? [6/36 = 1/6]
3. P(sum = 12)? [1/36]

Level 4: Complex Probability
---------------------------
🎯 Master Challenge:
Q: Rolling two dice:
1. P(first die > second die)?
2. P(product is even)?
3. P(sum is prime)?

[Try solving these before looking at answers!]

Answers:
1. 15/36 = 5/12
2. 27/36 = 3/4
3. 15/36 = 5/12 (sum of 2,3,5,7,11)

Level 5: Real-world Applications
------------------------------
🎯 Application Challenges:
1. If you flip 3 coins, what's more likely:
   * All heads
   * Two heads and one tail
   [Work it out!]

2. In a game with two dice:
   * Is sum=7 or sum=6 more likely?
   * Why?
   [Think about possible combinations]

💡 Probability Principles:
Q: What patterns have you noticed?
1. All probabilities are between 0 and 1
2. More complex events often have lower probabilities
3. Multiple ways to reach same outcome increase probability

🌟 Bonus Challenges:
1. Create a probability problem involving 3 dice
2. Find the probability of rolling three 6's in a row
3. Calculate the probability of NOT rolling a 6 in 4 tries

Want to explore more?
1. How does probability relate to statistics?
2. Can you explain conditional probability?
3. What's the difference between theoretical and experimental probability?"""
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
logger = logging.getLogger("demo_07")


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


def analyze_questions(results: List[Dict]) -> Dict:
    """Analyze effectiveness of question types."""
    analysis = {
        "overall_scores": {},
        "question_types": {},
        "type_effectiveness": {},
        "recommendations": []
    }
    
    # Track question types
    type_scores = {
        "conceptual": [],
        "procedural": [],
        "analytical": [],
        "application": [],
        "verification": []
    }
    
    for result in results:
        style = result["style"]
        scores = result["scores"]
        output = result["output"].lower()
        
        # Overall scores
        analysis["overall_scores"][style] = scores["total_score"]
        
        # Track question types used
        types_used = []
        if "why" in output or "what happens" in output or "understand" in output:
            types_used.append("conceptual")
            type_scores["conceptual"].append(scores["total_score"])
        if "how" in output or "step" in output or "calculate" in output:
            types_used.append("procedural")
            type_scores["procedural"].append(scores["total_score"])
        if "pattern" in output or "compare" in output or "analyze" in output:
            types_used.append("analytical")
            type_scores["analytical"].append(scores["total_score"])
        if "real-world" in output or "apply" in output or "example" in output:
            types_used.append("application")
            type_scores["application"].append(scores["total_score"])
        if "check" in output or "verify" in output or "confirm" in output:
            types_used.append("verification")
            type_scores["verification"].append(scores["total_score"])
        
        analysis["question_types"][style] = types_used
    
    # Analyze type effectiveness
    for qtype, scores in type_scores.items():
        if scores:
            analysis["type_effectiveness"][qtype] = sum(scores) / len(scores)
    
    # Generate recommendations
    sorted_types = sorted(
        analysis["type_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    analysis["recommendations"].extend([
        f"Most effective type: {sorted_types[0][0]} ({sorted_types[0][1]:.2f})",
        "Balance different question types",
        "Start with conceptual understanding",
        "Include real-world applications",
        "End with verification questions"
    ])
    
    return analysis


def display_results(results: List[Dict], analysis: Dict):
    """Display results and analysis."""
    # Scores table
    scores_table = Table(title="Question Types Analysis")
    scores_table.add_column("Style", style="cyan")
    scores_table.add_column("Total Score", style="green")
    scores_table.add_column("Question Types", style="yellow")
    
    for result in results:
        style = result["style"]
        types = analysis["question_types"][style]
        scores_table.add_row(
            style,
            f"{analysis['overall_scores'][style]:.2f}",
            "\n".join(types)
        )
    
    # Types table
    types_table = Table(title="Question Type Effectiveness")
    types_table.add_column("Type", style="cyan")
    types_table.add_column("Average Score", style="green")
    
    for qtype, score in sorted(
        analysis["type_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        types_table.add_row(
            qtype.title(),
            f"{score:.2f}"
        )
    
    # Recommendations table
    recommendations_table = Table(title="Best Practices")
    recommendations_table.add_column("Category", style="cyan")
    recommendations_table.add_column("Details", style="yellow")
    
    recommendations_table.add_row(
        "Top Type",
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
    console.print(types_table)
    console.print("\n")
    console.print(recommendations_table)


def save_results(results: Dict):
    """Save results to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "demo_07_results.json"
    
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
            console.print("\n[bold]Testing Question Types[/bold]")
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
                analysis = analyze_questions(scored_cases)
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
    console.print("\n[bold]Running Demo 7: Question Types Analysis[/bold]")
    asyncio.run(main()) 