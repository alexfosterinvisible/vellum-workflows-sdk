"""
Contract Testing Probe - Test PI API contract generation and scoring.

This module provides:
1. Contract generation testing
2. Input measurement against contracts
3. Stability and consistency analysis
4. Pattern detection in scoring

v1 - Initial implementation with contract focus
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

import aiohttp
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel

# Configuration
API_KEY = "pilabs_key_epc8PlKUV7BzrsVJUJRzE3h3XLgxXa2zC6Hh7RSkIEo"
BASE_URL = "https://api.withpi.ai/v1"
OUTPUT_DIR = Path("contract_probe_results")

# API Endpoints from Swagger
ENDPOINTS = {
    "contracts": {
        "create": "/contracts",
        "list": "/contracts",
        "get": "/contracts/{contract_id}",
        "update": "/contracts/{contract_id}",
        "delete": "/contracts/{contract_id}",
        "evaluate": "/contracts/{contract_id}/evaluate",
        "dimensions": "/contracts/{contract_id}/dimensions"
    }
}

# Test Data
TEST_CONTRACTS = [
    {
        "name": "Math Skills Assessment",
        "description": "Evaluate mathematical problem-solving abilities",
        "evaluation_criteria": {
            "accuracy": "Solutions must be mathematically correct",
            "explanation": "Clear step-by-step explanations required",
            "efficiency": "Solutions should use optimal methods"
        }
    },
    {
        "name": "Code Review Quality",
        "description": "Assess code review feedback quality",
        "evaluation_criteria": {
            "thoroughness": "All code aspects must be reviewed",
            "clarity": "Feedback must be clear and actionable",
            "constructiveness": "Suggestions must be helpful and specific"
        }
    }
]

# Logging setup
console = Console()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("contract_probe")


class ContractProbe:
    """Probe for testing PI API contract generation and scoring.
    
    1. Tests contract creation and management
    2. Validates dimension generation
    3. Tests evaluation endpoints
    v1 - Initial implementation with Swagger-based endpoints
    """
    
    def __init__(self, api_key: str = API_KEY):
        """Initialize probe with API credentials.
        
        1. Set up authentication
        2. Configure logging
        3. Create output directory
        v1 - Basic setup with API key
        """
        self.api_key = api_key
        self.session = None
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        logger.debug(f"Initialized ContractProbe with API key: {self.api_key[:8]}...")
    
    async def __aenter__(self):
        """Set up async context with session."""
        self.session = aiohttp.ClientSession(headers=self.headers)
        logger.debug("Created aiohttp session")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up async context."""
        if self.session:
            await self.session.close()
            logger.debug("Closed aiohttp session")
    
    async def test_connection(self) -> bool:
        """Test API connection and authentication.
        
        1. Check API health
        2. Verify authentication
        3. Log response details
        v1 - Basic health check
        """
        try:
            # First try the root endpoint
            async with self.session.get(BASE_URL) as resp:
                logger.debug(f"Root endpoint response: {resp.status}")
                if resp.status == 200:
                    return True
            
            # If root fails, try listing contracts
            async with self.session.get(f"{BASE_URL}{ENDPOINTS['contracts']['list']}") as resp:
                logger.debug(f"List contracts response: {resp.status}")
                return resp.status in [200, 401]  # 401 means API is up but auth failed
        
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    async def create_test_contract(self, contract_data: Dict) -> Optional[str]:
        """Create a test contract.
        
        1. Send contract creation request
        2. Handle response
        3. Return contract ID if successful
        v1 - Basic contract creation
        """
        try:
            async with self.session.post(
                f"{BASE_URL}{ENDPOINTS['contracts']['create']}", 
                json=contract_data
            ) as resp:
                if resp.status == 201:
                    data = await resp.json()
                    contract_id = data.get("id")
                    logger.info(f"Created contract: {contract_id}")
                    return contract_id
                else:
                    text = await resp.text()
                    logger.error(f"Failed to create contract: {text}")
                    return None
        except Exception as e:
            logger.error(f"Error creating contract: {e}")
            return None
    
    async def get_contract_dimensions(self, contract_id: str) -> Optional[List[Dict]]:
        """Get dimensions for a contract.
        
        1. Fetch dimensions from API
        2. Parse response
        3. Return dimension list
        v1 - Basic dimension fetching
        """
        try:
            endpoint = ENDPOINTS['contracts']['dimensions'].format(contract_id=contract_id)
            async with self.session.get(f"{BASE_URL}{endpoint}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("dimensions", [])
                else:
                    text = await resp.text()
                    logger.error(f"Failed to get dimensions: {text}")
                    return None
        except Exception as e:
            logger.error(f"Error getting dimensions: {e}")
            return None
    
    def save_result(self, test_name: str, result: Dict):
        """Save test results to file.
        
        1. Create output file
        2. Write JSON data
        3. Log success/failure
        v1 - Basic result saving
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = OUTPUT_DIR / f"{test_name}_{timestamp}.json"
            with open(filename, "w") as f:
                json.dump(result, f, indent=2)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")


async def main():
    """Main execution function.
    
    1. Test API connection
    2. Create test contracts
    3. Analyze dimensions
    v1 - Basic testing flow
    """
    try:
        async with ContractProbe() as probe:
            # Test connection
            if await probe.test_connection():
                console.print(Panel("[green]API connection successful![/green]"))
                
                # Create test contracts
                results = {"contracts": [], "dimensions": []}
                for contract in TEST_CONTRACTS:
                    if contract_id := await probe.create_test_contract(contract):
                        results["contracts"].append({
                            "id": contract_id,
                            "contract": contract
                        })
                        
                        # Get dimensions
                        if dimensions := await probe.get_contract_dimensions(contract_id):
                            results["dimensions"].append({
                                "contract_id": contract_id,
                                "dimensions": dimensions
                            })
                
                # Save results
                probe.save_result("api_test", results)
            else:
                console.print(Panel("[red]API connection failed![/red]"))
    
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    asyncio.run(main())