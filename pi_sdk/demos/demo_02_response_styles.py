"""Demo 2: Response Style Comparison.

This demo shows:
1. Testing different response styles
2. Analyzing score patterns
3. Identifying high-scoring patterns
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
    "name": "Math Response Style Analysis",
    "description": """Evaluate different styles of mathematical explanations.
    Focus on clarity, completeness, and effectiveness of communication."""
}

TEST_CASES = [
    {
        "style": "Direct Answer",
        "input": "What is 15 divided by 3?",
        "output": "15 divided by 3 equals 5."
    },
    {
        "style": "Step by Step",
        "input": "What is 15 divided by 3?",
        "output": """Let me solve this step by step:
1. We start with 15 as our dividend
2. We need to divide it by 3 (our divisor)
3. 15 ÷ 3 = 5 because 3 × 5 = 15

Therefore, 15 divided by 3 equals 5."""
    },
    {
        "style": "Visual Style",
        "input": "What is 15 divided by 3?",
        "output": """Let's visualize this division:

15 ÷ 3 = ?

[15] → split into 3 equal groups → [5] [5] [5]

We can see that when we split 15 into 3 equal groups,
each group has 5 items.

Therefore, 15 divided by 3 equals 5."""
    },
    {
        "style": "Conceptual Explanation",
        "input": "What is 15 divided by 3?",
        "output": """Let me explain division conceptually:

Division is about splitting a number into equal groups.
In this case, we're splitting 15 into 3 equal groups.

Think of it like sharing 15 candies among 3 friends:
- Friend 1 gets 5 candies
- Friend 2 gets 5 candies
- Friend 3 gets 5 candies

This shows us that 15 ÷ 3 = 5, because each of the 3 groups gets 5 items."""
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
logger = logging.getLogger("demo_02")


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


def display_results(results: List[Dict]):
    """Display results in a table."""
    table = Table(title="Response Style Comparison")
    
    # Add columns
    table.add_column("Style", style="cyan")
    table.add_column("Total Score", style="green")
    table.add_column("Top Dimensions", style="yellow")
    table.add_column("Low Dimensions", style="red")
    
    # Add rows
    for result in results:
        # Get top and bottom dimensions
        dim_scores = result["scores"]["dimension_scores"]
        sorted_dims = sorted(
            [(k, v["total_score"]) for k, v in dim_scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        top_dims = [f"{d[0]} ({d[1]:.2f})" for d in sorted_dims[:2]]
        low_dims = [f"{d[0]} ({d[1]:.2f})" for d in sorted_dims[-2:]]
        
        table.add_row(
            result["style"],
            f"{result['scores']['total_score']:.2f}",
            "\n".join(top_dims),
            "\n".join(low_dims)
        )
    
    console.print(table)


def save_results(results: Dict):
    """Save results to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "demo_02_results.json"
    
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
            console.print("\n[bold]Testing Response Styles[/bold]")
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
            
            # Display results
            if scored_cases:
                console.print("\n[bold]Results Summary[/bold]")
                display_results(scored_cases)
                results["success"] = True
        
        # Save results
        save_results(results)
        
        if results["success"]:
            console.print("\n[bold green]Demo completed successfully![/bold green]")
        else:
            console.print("\n[bold red]Demo failed![/bold red]")


if __name__ == "__main__":
    console.print("\n[bold]Running Demo 2: Response Style Comparison[/bold]")
    asyncio.run(main()) 