"""Simple script to test PI API connection.

This module provides:
1. API connection testing
2. Authentication verification
3. Basic endpoint testing
v1 - Initial implementation with OpenAPI spec
"""

import asyncio
import json
import logging
from typing import Dict, Optional

import aiohttp
from rich.console import Console
from rich.logging import RichHandler

# Configuration
API_KEY = "pilabs_key_epc8PlKUV7BzrsVJUJRzE3h3XLgxXa2zC6Hh7RSkIEo"
BASE_URL = "https://api.withpi.ai/v1"

# Test data
TEST_CONTRACT = {
    "name": "Math Skills Assessment",
    "description": "Evaluate mathematical problem-solving abilities",
    "evaluation_criteria": {
        "accuracy": "Solutions must be mathematically correct",
        "explanation": "Clear step-by-step explanations required",
        "efficiency": "Solutions should use optimal methods"
    }
}

# Logging setup
console = Console()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("api_test")


async def generate_dimensions(session: aiohttp.ClientSession) -> Optional[Dict]:
    """Generate dimensions for the test contract."""
    url = f"{BASE_URL}/contracts/generate_dimensions"
    try:
        logger.debug(f"\nGenerating dimensions: {url}")
        logger.debug(f"Data: {json.dumps({'contract': TEST_CONTRACT}, indent=2)}")
        
        async with session.post(url, json={"contract": TEST_CONTRACT}) as resp:
            if resp.status == 200:
                data = await resp.json()
                logger.debug(f"Generated dimensions: {json.dumps(data, indent=2)}")
                return data
            else:
                text = await resp.text()
                logger.error(f"Failed to generate dimensions: {text}")
                return None
    except Exception as e:
        logger.error(f"Error generating dimensions: {e}")
        return None


async def test_contract_scoring(
    session: aiohttp.ClientSession,
    contract_with_dimensions: Dict
) -> bool:
    """Test contract scoring with dimensions."""
    url = f"{BASE_URL}/contracts/score"
    try:
        data = {
            "contract": contract_with_dimensions,
            "llm_input": "What is 2 + 2?",
            "llm_output": "The answer is 4. Let me explain step by step:\n1. We start with the numbers 2 and 2\n2. Using addition, we combine these numbers\n3. 2 + 2 equals 4\nTherefore, the answer is 4."
        }
        
        logger.debug(f"\nTesting contract scoring: {url}")
        logger.debug(f"Data: {json.dumps(data, indent=2)}")
        
        async with session.post(url, json=data) as resp:
            status = resp.status
            text = await resp.text()
            logger.debug(f"Status: {status}")
            logger.debug(f"Response: {text}")
            
            if status == 200:
                console.print("[green]✓ Contract Scoring - OK[/green]")
                return True
            else:
                console.print(f"[red]✗ Contract Scoring - Failed ({status})[/red]")
                return False
    
    except Exception as e:
        logger.error(f"Error testing contract scoring: {e}")
        console.print(f"[red]✗ Contract Scoring - Error: {str(e)}[/red]")
        return False


async def main():
    """Main execution function."""
    console.print("\n[bold]Testing PI API Connection[/bold]\n")
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        # First generate dimensions
        if contract_with_dimensions := await generate_dimensions(session):
            console.print("[green]✓ Generate Dimensions - OK[/green]")
            
            # Then test scoring
            await test_contract_scoring(session, contract_with_dimensions)
        else:
            console.print("[red]✗ Generate Dimensions - Failed[/red]")


if __name__ == "__main__":
    asyncio.run(main()) 