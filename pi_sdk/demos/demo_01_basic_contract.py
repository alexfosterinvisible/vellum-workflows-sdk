"""Demo 1: Basic Contract Generation and Scoring.

This demo shows:
1. Creating a basic math evaluation contract
2. Generating scoring dimensions
3. Testing with a simple math problem
v1 - Initial implementation
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Optional

import aiohttp
from rich.console import Console
from rich.logging import RichHandler

# Configuration
API_KEY = "pilabs_key_epc8PlKUV7BzrsVJUJRzE3h3XLgxXa2zC6Hh7RSkIEo"
BASE_URL = "https://api.withpi.ai/v1"
OUTPUT_DIR = Path("demo_results")

# Test data
MATH_CONTRACT = {
    "name": "Basic Math Evaluation",
    "description": """Evaluate responses to basic math problems.
    Focus on accuracy, step-by-step explanation, and clarity of presentation."""
}

TEST_CASES = [
    {
        "input": "What is 7 + 3?",
        "output": """Let me solve this step by step:
1. We start with 7
2. We need to add 3 to it
3. 7 + 3 = 10

Therefore, 7 + 3 equals 10."""
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
logger = logging.getLogger("demo_01")


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


def save_results(results: Dict):
    """Save results to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "demo_01_results.json"

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
            console.print("\n[bold]Testing Cases[/bold]")
            for case in TEST_CASES:
                if scores := await score_response(session, contract_with_dims, case):
                    results["test_cases"].append({
                        "input": case["input"],
                        "output": case["output"],
                        "scores": scores
                    })
                    console.print(f"[green]✓ Scored case: {case['input']}[/green]")
                    console.print(f"Total Score: {scores['total_score']:.2f}")

            results["success"] = True

        # Save results
        save_results(results)

        if results["success"]:
            console.print("\n[bold green]Demo completed successfully![/bold green]")
        else:
            console.print("\n[bold red]Demo failed![/bold red]")


if __name__ == "__main__":
    console.print("\n[bold]Running Demo 1: Basic Contract Testing[/bold]")
    asyncio.run(main())
