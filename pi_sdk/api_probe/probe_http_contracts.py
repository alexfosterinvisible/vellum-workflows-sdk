"""
Contract Testing Probe - Test PI API contract generation and scoring.

This module provides:
1. Contract generation testing
2. Input measurement against contracts
3. Stability and consistency analysis
4. Pattern detection in scoring

Usage:
    python probe_http_contracts.py --api-key YOUR_KEY
    python probe_http_contracts.py --api-key YOUR_KEY --test contract_evolution
    python probe_http_contracts.py --api-key YOUR_KEY --test score_distribution

v1 - Initial implementation with contract focus
"""

import argparse
import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

import aiohttp
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Global configuration
API_KEY = "pilabs_key_epc8PlKUV7BzrsVJUJRzE3h3XLgxXa2zC6Hh7RSkIEo"
BASE_URL = "https://api.withpi.ai/v1"
OUTPUT_DIR = Path("contract_probe_results")

# Test data - Contract Evolution
SIMILAR_CONTRACTS = [
    {
        "name": "Math Evaluation",
        "description": "Test mathematical problem solving ability with focus on arithmetic operations and numerical accuracy"
    },
    {
        "name": "Math Assessment",
        "description": "Evaluate capability in solving math problems, particularly basic arithmetic and numerical precision"
    },
    {
        "name": "Math Test",
        "description": "Check proficiency in mathematical calculations and arithmetic problem solving"
    },
    {
        "name": "Math Skills",
        "description": "Assess mathematical abilities focusing on basic operations and numerical solutions"
    }
]

# Test data - Edge Cases
EDGE_CASE_CONTRACTS = [
    {
        "name": "",
        "description": ""
    },
    {
        "name": "Very Long Name " * 50,
        "description": "Very Long Description " * 100
    },
    {
        "name": "Special !@#$%^&*()",
        "description": "Special Characters !@#$%^&*()"
    },
    {
        "name": "Minimal",
        "description": "Test"
    },
    {
        "name": "Unicode Test 测试",
        "description": "Testing unicode characters 测试 🚀 👍"
    }
]

# Test data - Input Scoring
TEST_INPUTS = [
    # Perfect match cases
    {
        "type": "perfect_match",
        "input": "What is 2 + 2?",
        "output": "The answer is 4.",
        "expected_range": (0.9, 1.0),
        "description": "Basic arithmetic with direct answer"
    },
    {
        "type": "perfect_match",
        "input": "Calculate 15 divided by 3",
        "output": "15 divided by 3 equals 5",
        "expected_range": (0.9, 1.0),
        "description": "Division with clear explanation"
    },
    # Partial match cases
    {
        "type": "partial_match",
        "input": "What is the sum of 2 and 3?",
        "output": "Let me think about that...",
        "expected_range": (0.4, 0.6),
        "description": "Incomplete answer"
    },
    {
        "type": "partial_match",
        "input": "Solve: 10 - 7",
        "output": "The numbers are 10 and 7",
        "expected_range": (0.4, 0.6),
        "description": "Related but not solving"
    },
    # No match cases
    {
        "type": "no_match",
        "input": "Tell me a joke",
        "output": "Why did the chicken cross the road?",
        "expected_range": (0.0, 0.2),
        "description": "Completely unrelated"
    },
    {
        "type": "no_match",
        "input": "What's the weather like?",
        "output": "It's sunny today!",
        "expected_range": (0.0, 0.2),
        "description": "Off-topic response"
    }
]

# Console setup with debug logging
console = Console()
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more verbose output
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("contract_probe")


class ContractProbe:
    """Probe for testing PI API contract generation and scoring.
    
    1. Tests contract generation consistency
    2. Analyzes dimension patterns
    3. Tests edge cases and error handling
    4. Measures scoring distribution
    v1 - Initial implementation with basic probing capabilities
    """
    
    def __init__(self, api_key: str = API_KEY):
        """Initialize the contract probe.
        
        1. Set up API credentials
        2. Initialize aiohttp session
        3. Create output directory
        v1 - Basic initialization with API key
        """
        self.api_key = api_key
        self.session = None
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Log configuration
        logger.debug(f"Initialized ContractProbe with API key: {self.api_key[:8]}...")
        logger.debug(f"Base URL: {BASE_URL}")
        logger.debug(f"Headers: {json.dumps(self.headers, indent=2)}")
        
        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    async def __aenter__(self):
        """Set up async context with debug logging."""
        self.session = aiohttp.ClientSession(headers=self.headers)
        logger.debug("Created aiohttp session")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up async context with debug logging."""
        if self.session:
            await self.session.close()
            logger.debug("Closed aiohttp session")
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make an API request with debug logging.
        
        1. Log request details
        2. Make request with retry logic
        3. Log response details
        v1 - Basic request handling with logging
        """
        url = f"{BASE_URL}{endpoint}"
        logger.debug(f"Making {method} request to {url}")
        logger.debug(f"Request kwargs: {json.dumps(kwargs, indent=2)}")
        
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                async with getattr(self.session, method.lower())(url, **kwargs) as resp:
                    logger.debug(f"Response status: {resp.status}")
                    logger.debug(f"Response headers: {dict(resp.headers)}")
                    
                    response_text = await resp.text()
                    logger.debug(f"Response text: {response_text}")
                    
                    if resp.status == 200:
                        return await resp.json()
                    elif resp.status == 401:
                        logger.error("Authentication failed. Please check your API key.")
                        raise Exception("Authentication failed")
                    else:
                        logger.error(f"Request failed with status {resp.status}: {response_text}")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(retry_delay * (attempt + 1))
                            continue
                        raise Exception(f"Request failed after {max_retries} attempts")
            
            except Exception as e:
                logger.error(f"Request error on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                raise
        
        raise Exception("Request failed after all retries")
    
    def save_result(self, test_name: str, result: Dict):
        """Save test results to JSON file.
        
        1. Create timestamped filename
        2. Write results with formatting
        3. Log success/failure
        v1 - Basic JSON file saving
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = OUTPUT_DIR / f"{test_name}_{timestamp}.json"
        
        try:
            with open(filename, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
    
    async def test_contract_evolution(self) -> Dict:
        """Test contract generation evolution with similar inputs.
        
        1. Test similar contracts for consistency
        2. Analyze dimension stability
        3. Track timing patterns
        v1 - Basic evolution testing with similar contracts
        """
        results = {
            "evolution_patterns": [],
            "timing_analysis": {},
            "stability_metrics": {}
        }
        
        # Test evolution across similar contracts
        for contract in SIMILAR_CONTRACTS:
            try:
                start_time = time.time()
                async with self.session.post(
                    f"{BASE_URL}/contracts/generate_dimensions",
                    json={"contract": contract}
                ) as resp:
                    duration = time.time() - start_time
                    
                    if resp.status == 200:
                        data = await resp.json()
                        dimensions = data.get("dimensions", [])
                        
                        results["evolution_patterns"].append({
                            "contract": contract,
                            "dimensions": dimensions,
                            "dimension_count": len(dimensions),
                            "timing": duration
                        })
                    else:
                        error_text = await resp.text()
                        logger.error(f"Error for contract {contract['name']}: {error_text}")
            
            except Exception as e:
                logger.error(f"Failed to test contract {contract['name']}: {e}")
        
        # Analyze stability across similar contracts
        if results["evolution_patterns"]:
            dimension_counts = [p["dimension_count"] for p in results["evolution_patterns"]]
            avg_dimensions = sum(dimension_counts) / len(dimension_counts)
            dimension_variance = sum((c - avg_dimensions) ** 2 for c in dimension_counts) / len(dimension_counts)
            
            results["stability_metrics"] = {
                "average_dimensions": avg_dimensions,
                "dimension_variance": dimension_variance,
                "dimension_range": {
                    "min": min(dimension_counts),
                    "max": max(dimension_counts)
                }
            }
        
        return results
    
    async def test_edge_cases(self) -> Dict:
        """Test contract generation with edge cases.
        
        1. Test extreme inputs
        2. Test special characters
        3. Test length variations
        v1 - Basic edge case testing
        """
        results = {
            "edge_case_results": [],
            "error_patterns": {},
            "response_analysis": {}
        }
        
        for case in EDGE_CASE_CONTRACTS:
            try:
                async with self.session.post(
                    f"{BASE_URL}/contracts/generate_dimensions",
                    json={"contract": case}
                ) as resp:
                    status = resp.status
                    response_text = await resp.text()
                    
                    try:
                        response_data = await resp.json() if status == 200 else None
                    except:
                        response_data = None
                    
                    results["edge_case_results"].append({
                        "case": case,
                        "status": status,
                        "response": response_data if response_data else response_text
                    })
                    
                    # Track error patterns
                    if status != 200:
                        if status not in results["error_patterns"]:
                            results["error_patterns"][status] = []
                        results["error_patterns"][status].append({
                            "case": case,
                            "error": response_text
                        })
            
            except Exception as e:
                logger.error(f"Failed to test edge case {case['name']}: {e}")
                results["edge_case_results"].append({
                    "case": case,
                    "error": str(e)
                })
        
        # Analyze response patterns
        success_count = len([r for r in results["edge_case_results"] if r.get("status") == 200])
        results["response_analysis"] = {
            "success_rate": success_count / len(EDGE_CASE_CONTRACTS),
            "error_distribution": {
                status: len(cases) 
                for status, cases in results["error_patterns"].items()
            }
        }
        
        return results
    
    async def test_score_distribution(self) -> Dict:
        """Test contract scoring distribution."""
        results = {
            "score_patterns": [],
            "distribution_analysis": {}
        }
        
        # Generate a test contract first
        async with self.session.post(
            f"{BASE_URL}/contracts/generate_dimensions",
            json={
                "contract": {
                    "name": "Test Contract",
                    "description": "A test contract for score distribution analysis"
                }
            }
        ) as resp:
            contract = await resp.json()
        
        # Test different inputs against the contract
        for test_case in TEST_INPUTS:
            scores = []
            # Test each input multiple times for stability
            for _ in range(5):
                async with self.session.post(
                    f"{BASE_URL}/contracts/score",
                    json={
                        "contract": contract,
                        "llm_input": test_case["input"],
                        "llm_output": test_case["output"]
                    }
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        scores.append(data.get("total_score", 0))
            
            results["score_patterns"].append({
                "test_case": test_case,
                "scores": scores,
                "mean_score": sum(scores) / len(scores) if scores else 0,
                "score_variance": sum((s - (sum(scores) / len(scores))) ** 2 for s in scores) / len(scores) if scores else 0
            })
        
        # Analyze score distribution
        all_scores = [score for pattern in results["score_patterns"] for score in pattern["scores"]]
        results["distribution_analysis"] = {
            "min_score": min(all_scores),
            "max_score": max(all_scores),
            "mean_score": sum(all_scores) / len(all_scores),
            "score_ranges": {
                "0.0-0.2": len([s for s in all_scores if 0.0 <= s <= 0.2]),
                "0.2-0.4": len([s for s in all_scores if 0.2 < s <= 0.4]),
                "0.4-0.6": len([s for s in all_scores if 0.4 < s <= 0.6]),
                "0.6-0.8": len([s for s in all_scores if 0.6 < s <= 0.8]),
                "0.8-1.0": len([s for s in all_scores if 0.8 < s <= 1.0])
            }
        }
        
        return results
    
    async def test_contract_variations(self) -> Dict:
        """Test contract generation with various combinations."""
        results = {
            "variations": [],
            "timing_analysis": {},
            "dimension_patterns": {},
            "error_cases": []
        }
        
        # Test cases for systematic exploration
        test_cases = [
            # Basic math contracts with increasing complexity
            {
                "name": "Basic Math",
                "description": "Test basic arithmetic operations"
            },
            {
                "name": "Advanced Math",
                "description": "Test complex mathematical operations including algebra and calculus"
            },
            # Language variation tests
            {
                "name": "Math in English",
                "description": "Test mathematical calculations with English descriptions"
            },
            {
                "name": "Math 数学",
                "description": "Test math with Unicode characters 测试数学计算"
            },
            # Length variation tests
            {
                "name": "M",
                "description": "S"
            },
            {
                "name": "Math Test " * 10,
                "description": "Test mathematical abilities " * 10
            }
        ]
        
        for case in test_cases:
            try:
                start_time = time.time()
                async with self.session.post(
                    f"{BASE_URL}/contracts/generate_dimensions",
                    json={"contract": case}
                ) as resp:
                    duration = time.time() - start_time
                    status = resp.status
                    
                    if status == 200:
                        data = await resp.json()
                        dimensions = data.get("dimensions", [])
                        
                        # Analyze dimension patterns
                        dim_count = len(dimensions)
                        dim_labels = [d.get("label") for d in dimensions]
                        has_subdims = any(
                            d.get("sub_dimensions") for d in dimensions
                        )
                        
                        results["variations"].append({
                            "case": case,
                            "status": status,
                            "duration": duration,
                            "dimension_count": dim_count,
                            "dimension_labels": dim_labels,
                            "has_subdimensions": has_subdims,
                            "response": data
                        })
                    else:
                        error_text = await resp.text()
                        results["error_cases"].append({
                            "case": case,
                            "status": status,
                            "error": error_text
                        })
                    
                    results["timing_analysis"][str(case)] = duration
            
            except Exception as e:
                results["error_cases"].append({
                    "case": case,
                    "error": str(e)
                })
        
        # Analyze patterns in dimensions
        all_labels = []
        for var in results["variations"]:
            all_labels.extend(var.get("dimension_labels", []))
        
        from collections import Counter
        label_frequency = Counter(all_labels)
        
        results["dimension_patterns"] = {
            "common_labels": dict(label_frequency.most_common(5)),
            "unique_labels": len(set(all_labels)),
            "total_labels": len(all_labels),
            "average_dimensions": sum(
                var["dimension_count"] 
                for var in results["variations"] 
                if "dimension_count" in var
            ) / len(results["variations"]) if results["variations"] else 0
        }
        
        return results
    
    async def run_all_tests(self):
        """Run all contract probe tests."""
        try:
            console.print("\n[bold magenta]Running Contract Probe Tests[/bold magenta]\n")
            
            # Test contract evolution
            console.print(Panel("Testing Contract Evolution", style="blue"))
            evolution_results = await self.test_contract_evolution()
            self.save_result("contract_evolution", evolution_results)
            
            # Test contract variations
            console.print(Panel("Testing Contract Variations", style="blue"))
            variation_results = await self.test_contract_variations()
            self.save_result("contract_variations", variation_results)
            
            # Test edge cases
            console.print(Panel("Testing Edge Cases", style="blue"))
            edge_case_results = await self.test_edge_cases()
            self.save_result("edge_cases", edge_case_results)
            
            # Test score distribution
            console.print(Panel("Testing Score Distribution", style="blue"))
            score_results = await self.test_score_distribution()
            self.save_result("score_distribution", score_results)
            
            console.print("\n[bold green]All contract tests completed![/bold green]")
        
        except Exception as e:
            console.print(f"\n[red]Error running contract tests: {str(e)}[/red]")
            raise


def parse_args():
    """Parse command line arguments.
    
    1. Parse API key
    2. Parse test selection
    3. Return parsed arguments
    v1 - Basic argument parsing
    """
    parser = argparse.ArgumentParser(description="PI API Contract Probe")
    parser.add_argument(
        "--api-key",
        default=API_KEY,
        help="PI API key (default: uses environment variable)"
    )
    parser.add_argument(
        "--test",
        choices=[
            "contract_evolution",
            "edge_cases",
            "score_distribution",
            "contract_variations",
            "all"
        ],
        default="all",
        help="Specific test to run (default: all)"
    )
    return parser.parse_args()


async def main():
    """Main execution function.
    
    1. Parse arguments
    2. Initialize probe
    3. Run selected tests
    4. Handle errors
    v1 - Basic execution flow
    """
    args = parse_args()
    
    try:
        async with ContractProbe(api_key=args.api_key) as probe:
            if args.test == "all":
                await probe.run_all_tests()
            elif args.test == "contract_evolution":
                results = await probe.test_contract_evolution()
                probe.save_result("contract_evolution", results)
            elif args.test == "edge_cases":
                results = await probe.test_edge_cases()
                probe.save_result("edge_cases", results)
            elif args.test == "score_distribution":
                results = await probe.test_score_distribution()
                probe.save_result("score_distribution", results)
            elif args.test == "contract_variations":
                results = await probe.test_contract_variations()
                probe.save_result("contract_variations", results)
    
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        raise


if __name__ == "__main__":
    asyncio.run(main()) 