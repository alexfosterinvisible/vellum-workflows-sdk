"""Demo 3: Hybrid Response Optimization.

This demo shows:
1. Combining best elements from different styles
2. Testing hybrid response patterns
3. Analyzing dimension optimization
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
    "name": "Math Response Optimization",
    "description": """Evaluate hybrid mathematical explanations.
    Focus on combining visual, conceptual, and step-by-step approaches
    to maximize understanding and engagement."""
}

TEST_CASES = [
    {
        "style": "Step-by-Step with Visuals",
        "input": "What is 12 divided by 4?",
        "output": """Let me solve this step by step with a visual representation:

1. We start with 12 items:
   [*] [*] [*] [*] [*] [*] [*] [*] [*] [*] [*] [*]

2. We need to divide them into 4 equal groups:
   Group 1: [*] [*] [*]
   Group 2: [*] [*] [*]
   Group 3: [*] [*] [*]
   Group 4: [*] [*] [*]

3. Counting the items in each group:
   Each group has exactly 3 items.

Therefore, 12 ÷ 4 = 3, because when we split 12 items into 4 equal groups,
each group gets 3 items.

To verify: 4 × 3 = 12 ✓"""
    },
    {
        "style": "Conceptual with Steps",
        "input": "What is 12 divided by 4?",
        "output": """Let me explain this both conceptually and systematically:

📚 Understanding Division:
Division is about splitting a larger quantity into equal smaller groups.
Think of sharing 12 cookies among 4 friends fairly.

Step-by-Step Solution:
1. Start with 12 cookies
2. Each friend should get the same amount
3. 12 ÷ 4 = 3 (each friend gets 3 cookies)

Real-world Application:
If you have $12 and want to spend it equally over 4 days,
you could spend $3 each day.

Verification:
- Each friend gets 3 cookies
- Total friends: 4
- Check: 4 × 3 = 12 ✓

Therefore, 12 divided by 4 equals 3."""
    },
    {
        "style": "Visual with Real-world",
        "input": "What is 12 divided by 4?",
        "output": """Let's solve this using a pizza-sharing visualization!

Starting Situation:
🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕 (12 slices total)

Sharing Plan:
Person 1: 🍕🍕🍕
Person 2: 🍕🍕🍕
Person 3: 🍕🍕🍕
Person 4: 🍕🍕🍕

Mathematical Expression:
12 slices ÷ 4 people = 3 slices per person

This shows that 12 divided by 4 equals 3.
Each person gets an equal share of 3 slices."""
    },
    {
        "style": "Complete Hybrid",
        "input": "What is 12 divided by 4?",
        "output": """Let's understand this completely using multiple approaches!

1. Visual Representation:
   12 items: ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
   Grouped into 4: [⭐⭐⭐] [⭐⭐⭐] [⭐⭐⭐] [⭐⭐⭐]

2. Step-by-Step Solution:
   a) Start with 12
   b) Divide into 4 equal groups
   c) Count items per group: 3
   d) Therefore, 12 ÷ 4 = 3

3. Real-world Example:
   Imagine having 12 candies to share with 4 friends.
   Each friend would get 3 candies.

4. Mathematical Verification:
   - Division: 12 ÷ 4 = 3
   - Multiplication check: 4 × 3 = 12 ✓
   - Addition check: 3 + 3 + 3 + 3 = 12 ✓

Key Concepts:
- Division is fair sharing
- Each group gets equal amount
- The result (3) represents the size of each group

Therefore, 12 divided by 4 equals 3."""
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
logger = logging.getLogger("demo_03")


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


def analyze_dimensions(results: List[Dict]) -> Dict[str, List[str]]:
    """Analyze dimension performance across styles."""
    analysis = {
        "top_dimensions": [],
        "needs_improvement": [],
        "style_strengths": {}
    }

    # Aggregate scores by dimension
    dimension_scores = {}
    for result in results:
        style = result["style"]
        scores = result["scores"]["dimension_scores"]

        # Track best dimensions for each style
        style_dims = sorted(
            [(k, v["total_score"]) for k, v in scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        analysis["style_strengths"][style] = [
            f"{d[0]} ({d[1]:.2f})"
            for d in style_dims[:2]
        ]

        # Aggregate dimension scores
        for dim, data in scores.items():
            if dim not in dimension_scores:
                dimension_scores[dim] = []
            dimension_scores[dim].append(data["total_score"])

    # Find overall top and bottom dimensions
    avg_scores = {
        dim: sum(scores) / len(scores)
        for dim, scores in dimension_scores.items()
    }

    sorted_dims = sorted(
        avg_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    analysis["top_dimensions"] = [
        f"{d[0]} ({d[1]:.2f})"
        for d in sorted_dims[:3]
    ]

    analysis["needs_improvement"] = [
        f"{d[0]} ({d[1]:.2f})"
        for d in sorted_dims[-3:]
    ]

    return analysis


def display_results(results: List[Dict], analysis: Dict):
    """Display results and analysis."""
    # Scores table
    scores_table = Table(title="Response Style Comparison")
    scores_table.add_column("Style", style="cyan")
    scores_table.add_column("Total Score", style="green")
    scores_table.add_column("Top Dimensions", style="yellow")

    for result in results:
        # Get top dimensions
        dim_scores = result["scores"]["dimension_scores"]
        sorted_dims = sorted(
            [(k, v["total_score"]) for k, v in dim_scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        top_dims = [f"{d[0]} ({d[1]:.2f})" for d in sorted_dims[:2]]

        scores_table.add_row(
            result["style"],
            f"{result['scores']['total_score']:.2f}",
            "\n".join(top_dims)
        )

    # Analysis table
    analysis_table = Table(title="Dimension Analysis")
    analysis_table.add_column("Category", style="cyan")
    analysis_table.add_column("Dimensions", style="yellow")

    analysis_table.add_row(
        "Top Performing",
        "\n".join(analysis["top_dimensions"])
    )
    analysis_table.add_row(
        "Needs Improvement",
        "\n".join(analysis["needs_improvement"])
    )

    # Style strengths table
    strengths_table = Table(title="Style Strengths")
    strengths_table.add_column("Style", style="cyan")
    strengths_table.add_column("Strong Dimensions", style="yellow")

    for style, dims in analysis["style_strengths"].items():
        strengths_table.add_row(
            style,
            "\n".join(dims)
        )

    # Display all tables
    console.print("\n")
    console.print(scores_table)
    console.print("\n")
    console.print(analysis_table)
    console.print("\n")
    console.print(strengths_table)


def save_results(results: Dict):
    """Save results to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "demo_03_results.json"

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
            console.print("\n[bold]Testing Hybrid Responses[/bold]")
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
                    console.print(f"[green]�� Scored {case['style']}[/green]")

            # Analyze and display results
            if scored_cases:
                analysis = analyze_dimensions(scored_cases)
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
    console.print("\n[bold]Running Demo 3: Hybrid Response Optimization[/bold]")
    asyncio.run(main())
