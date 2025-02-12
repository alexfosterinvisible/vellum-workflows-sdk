"""Demo 5: Complex Math Problem Analysis.

This demo shows:
1. Testing engagement patterns with complex problems
2. Analyzing scalability of response styles
3. Optimizing for problem complexity
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
    "name": "Complex Math Problem Analysis",
    "description": """Evaluate mathematical explanations for complex problems.
    Focus on maintaining engagement and clarity while handling increased complexity.
    Test effectiveness of different response styles with challenging concepts."""
}

TEST_CASES = [
    {
        "style": "Story-based Complex",
        "input": "If a recipe needs 2¾ cups of flour for 12 cookies, how many cups of flour are needed for 30 cookies?",
        "output": """🧁 Welcome to the Cookie Factory Challenge! 🏭

Our master baker Maria has a special recipe that makes exactly 12 delicious cookies.
She needs to scale it up for a big party order of 30 cookies!

Let's help Maria figure this out:

1. Current Recipe (12 cookies):
   🥄 Flour needed: 2¾ cups

2. Understanding the Problem:
   - We need to find flour for 30 cookies
   - Current recipe makes 12 cookies
   - We'll need to scale up the recipe!

3. Step-by-Step Solution:
   First, let's find flour per cookie:
   * 2¾ cups ÷ 12 cookies
   * 2.75 ÷ 12 = 0.229166... cups per cookie

   Now, for 30 cookies:
   * 0.229166... × 30 = 6.875 cups
   * 6.875 = 6⅞ cups

🎯 Final Answer: Maria needs 6⅞ cups of flour for 30 cookies.

✨ Bonus Baking Facts:
- This is about 2.5 times the original recipe
- You could measure this as 6 cups plus 7 tablespoons
- Pro bakers always scale recipes this way!

Want to test your skills? How much flour would you need for 45 cookies? 🤔"""
    },
    {
        "style": "Visual Complex",
        "input": "A cylindrical water tank has a radius of 3 meters and a height of 4 meters. What is its volume in cubic meters?",
        "output": """🌊 Let's Visualize This Water Tank! 🚰

1. The Tank's Shape:

         4m
   ┌──────┐  ↑
   │      │  │
   │      │  │ Height
3m │      │  │
   │      │  │
   └──────┘  ↓
   ←──→
  Radius

2. Understanding the Formula:
   Volume of a cylinder = π × radius² × height

   Think of it as:
   🔵 Area of the base (π × radius²)
   ↓
   📏 Multiplied by height

3. Let's Calculate:
   * radius = 3 meters
   * height = 4 meters
   * π ≈ 3.14159

   Step by step:
   1) radius² = 3² = 9
   2) π × 9 = 28.27431
   3) 28.27431 × 4 = 113.09724

🎯 Final Answer: The tank's volume is approximately 113.1 cubic meters

To visualize this volume:
- It's like 113,100 one-liter bottles! 🍶
- Or about 45 standard bathtubs! 🛁

💡 Real-world Application:
This tank could supply a small apartment building with water for several days!

Want to explore more? Try calculating:
1. How many 2-liter bottles could this tank fill?
2. If the radius was doubled, how would the volume change?"""
    },
    {
        "style": "Interactive Complex",
        "input": "Solve the equation: 3x + 7 = 4x - 5",
        "output": """🎮 Welcome to Equation Explorer! Let's solve this step by step.

Initial Equation: 3x + 7 = 4x - 5

🤔 Question: What should we do first?
[Think about it...]
Answer: Let's get all terms with x on one side!

Step 1: Subtract 3x from both sides
- Left side: 3x - 3x + 7 = 7
- Right side: 4x - 3x - 5 = x - 5
New equation: 7 = x - 5

🎯 Challenge: What's our next move?
[Consider your options...]
Solution: Add 5 to both sides!

Step 2: Add 5 to both sides
- Left side: 7 + 5 = 12
- Right side: x - 5 + 5 = x
Final equation: 12 = x

✨ Therefore: x = 12

Let's verify our answer:
Original equation: 3x + 7 = 4x - 5
Plug in x = 12:
- Left side: 3(12) + 7 = 36 + 7 = 43
- Right side: 4(12) - 5 = 48 - 5 = 43
43 = 43 ✓ It works!

🌟 Bonus Challenges:
1. Can you solve: 2x + 3 = x + 15?
2. What happens if we change 7 to -7?
3. Create your own equation with x = 5!

💡 Key Insights:
- Moving terms: What we do to one side, we must do to the other
- Verification is crucial: Always check your answer
- Multiple approaches can work: What's your preferred method?"""
    },
    {
        "style": "Guided Complex",
        "input": "Find the probability of rolling a sum of 8 with two dice.",
        "output": """🎲 Probability Explorer: Rolling for 8! 🎲

Step 1: Understanding the Problem
--------------------------------
Q: What are we looking for?
A: Ways to roll a sum of 8 using two dice

Q: What's our strategy?
A: List all possible combinations that sum to 8

Step 2: Finding Possibilities
----------------------------
Let's map it out:
Die 1 + Die 2 = 8

Possible combinations:
2 + 6 = 8  ⚁⚅
3 + 5 = 8  ⚂⚄
4 + 4 = 8  ⚃⚃
5 + 3 = 8  ⚄⚂
6 + 2 = 8  ⚅⚁

🤔 Think: Did we find all combinations?
Count them: 5 ways to roll an 8!

Step 3: Total Possible Outcomes
------------------------------
Q: How many possible outcomes when rolling 2 dice?
Let's count:
- Die 1: 6 possibilities
- Die 2: 6 possibilities
- Total: 6 × 6 = 36 possible outcomes

Step 4: Calculating Probability
-----------------------------
Probability = Favorable outcomes ÷ Total outcomes
            = 5 ÷ 36
            = 5/36 (approximately 0.139 or 13.9%)

🎯 Final Answer: The probability is 5/36

💡 Visualization:
     1  2  3  4  5  6
   +------------------
1  |2  3  4  5  6  7
2  |3  4  5  6  7  8*
3  |4  5  6  7  8* 9
4  |5  6  7  8* 9  10
5  |6  7  8* 9  10 11
6  |7  8* 9  10 11 12

* marks the combinations that sum to 8

🌟 Extension Questions:
1. Which sum is most likely when rolling 2 dice?
2. What's the probability of rolling a sum less than 8?
3. How would using 3 dice change our approach?

Remember: In probability, organizing possibilities systematically
helps us ensure we don't miss any outcomes!"""
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
logger = logging.getLogger("demo_05")


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


def analyze_complexity(results: List[Dict]) -> Dict:
    """Analyze how styles handle increased complexity."""
    analysis = {
        "overall_scores": {},
        "complexity_impact": {},
        "engagement_retention": {},
        "recommendations": []
    }

    # Track scores and patterns
    for result in results:
        style = result["style"]
        scores = result["scores"]
        output = result["output"]

        # Overall scores
        analysis["overall_scores"][style] = scores["total_score"]

        # Analyze complexity handling
        complexity_score = 0
        if "step by step" in output.lower():
            complexity_score += 0.2
        if any(marker in output for marker in ["therefore", "thus", "hence"]):
            complexity_score += 0.1
        if "verify" in output.lower() or "check" in output.lower():
            complexity_score += 0.2
        if "visualization" in output.lower() or "diagram" in output.lower():
            complexity_score += 0.2
        if "real-world" in output.lower() or "application" in output.lower():
            complexity_score += 0.2

        analysis["complexity_impact"][style] = complexity_score

        # Analyze engagement retention
        engagement_score = 0
        if "?" in output:
            engagement_score += 0.2
        if any(emoji in output for emoji in ["🌟", "⭐", "💡", "🎯"]):
            engagement_score += 0.2
        if "challenge" in output.lower():
            engagement_score += 0.2
        if "bonus" in output.lower():
            engagement_score += 0.2
        if "try" in output.lower() or "explore" in output.lower():
            engagement_score += 0.2

        analysis["engagement_retention"][style] = engagement_score

    # Generate recommendations
    sorted_styles = sorted(
        analysis["overall_scores"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_style = sorted_styles[0][0]
    top_score = sorted_styles[0][1]

    analysis["recommendations"].extend([
        f"Best performing style: {top_style} ({top_score:.2f})",
        f"Key elements: {', '.join(k for k, v in analysis['complexity_impact'].items() if v > 0.5)}",
        "Maintain engagement with regular checkpoints",
        "Use visual aids for complex concepts",
        "Include verification steps"
    ])

    return analysis


def display_results(results: List[Dict], analysis: Dict):
    """Display results and analysis."""
    # Scores table
    scores_table = Table(title="Complex Problem Analysis")
    scores_table.add_column("Style", style="cyan")
    scores_table.add_column("Total Score", style="green")
    scores_table.add_column("Complexity Score", style="yellow")
    scores_table.add_column("Engagement Score", style="magenta")

    for result in results:
        style = result["style"]
        scores_table.add_row(
            style,
            f"{analysis['overall_scores'][style]:.2f}",
            f"{analysis['complexity_impact'][style]:.2f}",
            f"{analysis['engagement_retention'][style]:.2f}"
        )

    # Recommendations table
    recommendations_table = Table(title="Style Recommendations")
    recommendations_table.add_column("Category", style="cyan")
    recommendations_table.add_column("Details", style="yellow")

    recommendations_table.add_row(
        "Best Style",
        analysis["recommendations"][0]
    )
    recommendations_table.add_row(
        "Key Elements",
        analysis["recommendations"][1]
    )
    recommendations_table.add_row(
        "Best Practices",
        "\n".join(analysis["recommendations"][2:])
    )

    # Display all tables
    console.print("\n")
    console.print(scores_table)
    console.print("\n")
    console.print(recommendations_table)


def save_results(results: Dict):
    """Save results to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "demo_05_results.json"

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
            console.print("\n[bold]Testing Complex Problems[/bold]")
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
                analysis = analyze_complexity(scored_cases)
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
    console.print("\n[bold]Running Demo 5: Complex Problem Analysis[/bold]")
    asyncio.run(main())
