"""Demo 6: Verification Methods Analysis.

This demo shows:
1. Testing different verification approaches
2. Analyzing effectiveness of proof methods
3. Optimizing solution validation
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
    "name": "Math Verification Methods",
    "description": """Evaluate mathematical explanations with a focus on verification.
    Test various proof and validation methods to identify the most effective
    approaches for ensuring solution correctness and understanding."""
}

TEST_CASES = [
    {
        "style": "Numerical Verification",
        "input": "Solve and verify: (x + 3)(x - 2) = x² + 5x - 6",
        "output": """Let's solve this step by step and verify our answer! 🔍

Step 1: Expand the left side (x + 3)(x - 2)
----------------------------------------
Using FOIL method:
* First: x × x = x²
* Outer: x × (-2) = -2x
* Inner: 3 × x = 3x
* Last: 3 × (-2) = -6

Combining terms:
(x + 3)(x - 2) = x² - 2x + 3x - 6
                = x² + x - 6

Step 2: Compare with right side
------------------------------
Left side: x² + x - 6
Right side: x² + 5x - 6

❌ They're not equal! The coefficients of x differ:
* Left side has: +1x
* Right side has: +5x

Therefore, the equation is FALSE.

🔢 Numerical Verification:
Let's test with x = 1:
* Left side: (1 + 3)(1 - 2) = (4)(-1) = -4
* Right side: 1² + 5(1) - 6 = 1 + 5 - 6 = 0

This confirms they're not equal!

✅ Double-Check:
1. Expanded correctly using FOIL
2. Combined like terms properly
3. Compared coefficients systematically
4. Verified with a numerical example

💡 Key Insight:
The equation is false because the coefficients of x don't match:
* (x + 3)(x - 2) = x² + x - 6
* x² + 5x - 6 has a different coefficient for x

Want to explore more? Try:
1. What value of x makes both sides closest to each other?
2. How would changing the 3 to 7 affect the equation?"""
    },
    {
        "style": "Algebraic Proof",
        "input": "Prove that (a + b)² = a² + 2ab + b²",
        "output": """Let's prove this algebraic identity step by step! 📝

Step 1: Setup the Proof
----------------------
We'll expand (a + b)² using the distributive property.
Remember: (a + b)² means (a + b)(a + b)

Step 2: Algebraic Expansion
--------------------------
Using FOIL method:
* First: a × a = a²
* Outer: a × b = ab
* Inner: b × a = ab
* Last: b × b = b²

Combining terms:
(a + b)² = a² + ab + ab + b²
         = a² + 2ab + b²

✅ Algebraic Verification:
1. Each term is accounted for
2. Like terms are combined correctly
3. Result matches the right side

🔢 Numerical Proof:
Let's verify with a = 2 and b = 3:

Left side: (2 + 3)²
* 2 + 3 = 5
* 5² = 25

Right side: 2² + 2(2)(3) + 3²
* 2² = 4
* 2(2)(3) = 12
* 3² = 9
* 4 + 12 + 9 = 25

Both sides equal 25! ✓

📊 Visual Proof:
Consider a square with side (a + b):
┌─────────┬───────┐
│    a²   │  ab   │
│         │       │
├─────────┼───────┤
│    ab   │  b²   │
│         │       │
└─────────┴───────┘

Area = a² + ab + ab + b² = a² + 2ab + b²

💡 Multiple Verifications:
1. Algebraic expansion ✓
2. Numerical example ✓
3. Geometric visualization ✓

Want to explore more?
1. Try different values for a and b
2. How does this relate to (a - b)²?
3. Can you visualize (a + b)³?"""
    },
    {
        "style": "Visual Verification",
        "input": "Prove that the sum of angles in a triangle is 180°",
        "output": """Let's prove this fundamental theorem visually! 👁️

Step 1: Visual Setup
-------------------
Consider any triangle ABC:
      A
      /\\
     /  \\
    /    \\
   /      \\
  /________\\
B           C

Step 2: Parallel Line Proof
--------------------------
1. Draw a line parallel to BC through point A:
      A
      /\\     ←  parallel line
     /  \\    _____________
    /    \\
   /      \\
  /________\\
B           C

2. Mark the angles:
      A
      /\\
     α  β    _____________
    /    \\
   /      \\
  /________\\
B     γ     C

✨ Key Observation:
* Angle α equals the original angle at B (alternate angles)
* Angle β equals the original angle at C (alternate angles)
* Angle γ is the original angle at A

3. At point A, these three angles form a straight line:
α + γ + β = 180° (angles on a straight line)

Therefore, the three angles of the original triangle
also sum to 180°!

🔢 Numerical Verification:
Let's check with a right triangle:
* Right angle = 90°
* One acute angle = 45°
* Other acute angle = 45°
* Total: 90° + 45° + 45° = 180° ✓

📐 Interactive Verification:
Try this:
1. Draw any triangle on paper
2. Cut out the three angles
3. Place them adjacent to each other
4. They form a straight line (180°)!

💡 Multiple Proofs:
1. Parallel line construction ✓
2. Numerical example ✓
3. Physical demonstration ✓

Want to explore more?
1. What happens in obtuse triangles?
2. How does this relate to exterior angles?
3. Can you extend this to other polygons?"""
    },
    {
        "style": "Logical Verification",
        "input": "Prove that if a number is divisible by 6, it must be divisible by both 2 and 3.",
        "output": """Let's prove this using logical reasoning! 🧠

Step 1: Understanding Divisibility
--------------------------------
A number n is divisible by 6 means:
* n = 6k, where k is some integer

Key fact: 6 = 2 × 3

Step 2: Logical Proof
--------------------
Given: n is divisible by 6
Therefore: n = 6k for some integer k

1. Divisibility by 2:
   n = 6k
   n = (2 × 3)k
   n = 2(3k)
   Let m = 3k (m is an integer because 3 and k are integers)
   Therefore: n = 2m
   ∴ n is divisible by 2 ✓

2. Divisibility by 3:
   n = 6k
   n = (2 × 3)k
   n = 3(2k)
   Let p = 2k (p is an integer because 2 and k are integers)
   Therefore: n = 3p
   ∴ n is divisible by 3 ✓

🔢 Numerical Verification:
Let's test with n = 24:
* 24 ÷ 6 = 4 (divisible by 6)
* 24 ÷ 2 = 12 (divisible by 2) ✓
* 24 ÷ 3 = 8 (divisible by 3) ✓

Let's test with n = 30:
* 30 ÷ 6 = 5 (divisible by 6)
* 30 ÷ 2 = 15 (divisible by 2) ✓
* 30 ÷ 3 = 10 (divisible by 3) ✓

✅ Multiple Verifications:
1. Algebraic proof ✓
2. Logical reasoning ✓
3. Numerical examples ✓

💡 Contrapositive:
If a number is NOT divisible by either 2 or 3,
it CANNOT be divisible by 6.
Example: 25 is not divisible by 2, so it can't be divisible by 6.

Want to explore more?
1. What about numbers divisible by 4 and 3?
2. How does this extend to other composite numbers?
3. Can you prove the contrapositive directly?"""
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
logger = logging.getLogger("demo_06")


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


def analyze_verification(results: List[Dict]) -> Dict:
    """Analyze effectiveness of verification methods."""
    analysis = {
        "overall_scores": {},
        "verification_methods": {},
        "method_effectiveness": {},
        "recommendations": []
    }

    # Track verification methods
    method_scores = {
        "numerical": [],
        "algebraic": [],
        "visual": [],
        "logical": [],
        "multiple": []
    }

    for result in results:
        style = result["style"]
        scores = result["scores"]
        output = result["output"].lower()

        # Overall scores
        analysis["overall_scores"][style] = scores["total_score"]

        # Track verification methods used
        methods_used = []
        if "numerical" in output or "example" in output:
            methods_used.append("numerical")
            method_scores["numerical"].append(scores["total_score"])
        if "algebraic" in output or "equation" in output:
            methods_used.append("algebraic")
            method_scores["algebraic"].append(scores["total_score"])
        if "visual" in output or "diagram" in output:
            methods_used.append("visual")
            method_scores["visual"].append(scores["total_score"])
        if "logic" in output or "proof" in output:
            methods_used.append("logical")
            method_scores["logical"].append(scores["total_score"])
        if len(methods_used) > 1:
            method_scores["multiple"].append(scores["total_score"])

        analysis["verification_methods"][style] = methods_used

    # Analyze method effectiveness
    for method, scores in method_scores.items():
        if scores:
            analysis["method_effectiveness"][method] = sum(scores) / len(scores)

    # Generate recommendations
    sorted_methods = sorted(
        analysis["method_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    analysis["recommendations"].extend([
        f"Most effective method: {sorted_methods[0][0]} ({sorted_methods[0][1]:.2f})",
        "Use multiple verification methods",
        "Include numerical examples",
        "Add visual aids when possible",
        "Verify both specific cases and general principles"
    ])

    return analysis


def display_results(results: List[Dict], analysis: Dict):
    """Display results and analysis."""
    # Scores table
    scores_table = Table(title="Verification Methods Analysis")
    scores_table.add_column("Style", style="cyan")
    scores_table.add_column("Total Score", style="green")
    scores_table.add_column("Methods Used", style="yellow")

    for result in results:
        style = result["style"]
        methods = analysis["verification_methods"][style]
        scores_table.add_row(
            style,
            f"{analysis['overall_scores'][style]:.2f}",
            "\n".join(methods)
        )

    # Methods table
    methods_table = Table(title="Method Effectiveness")
    methods_table.add_column("Method", style="cyan")
    methods_table.add_column("Average Score", style="green")

    for method, score in sorted(
        analysis["method_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        methods_table.add_row(
            method.title(),
            f"{score:.2f}"
        )

    # Recommendations table
    recommendations_table = Table(title="Best Practices")
    recommendations_table.add_column("Category", style="cyan")
    recommendations_table.add_column("Details", style="yellow")

    recommendations_table.add_row(
        "Top Method",
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
    console.print(methods_table)
    console.print("\n")
    console.print(recommendations_table)


def save_results(results: Dict):
    """Save results to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "demo_06_results.json"

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
            console.print("\n[bold]Testing Verification Methods[/bold]")
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
                analysis = analyze_verification(scored_cases)
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
    console.print("\n[bold]Running Demo 6: Verification Methods Analysis[/bold]")
    asyncio.run(main())
