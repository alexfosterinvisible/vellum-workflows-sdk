"""
PI API Probe - Test and explore the PI API endpoints.

This module provides:
1. Parallel test execution
2. Rate limiting
3. Response logging
4. Hypothesis validation

Usage:
    python probe.py
    python probe.py --output probe_2.md
    python probe.py --tests auth,inference

v2 - Added job management and dimension testing
"""

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
from rich.table import Table

# Global configuration
RATE_LIMIT_PER_MINUTE = 100
RATE_LIMIT_PER_SECOND = 30
BASE_URL = "https://api.pi.ai/v1"
OUTPUT_FILE = "probe_1.md"

# Test data
MINIMAL_CONTRACT = {
    "name": "test_contract",
    "description": "A test contract for quality evaluation",
    "dimensions": []
}

SAMPLE_INPUTS = [
    "What is the capital of France?",
    "Explain quantum computing",
    "Write a haiku about programming",
    "",  # Test empty input
    "A" * 1000  # Test long input
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("pi_probe")
console = Console()


class RateLimiter:
    """Rate limiter for API requests."""
    
    def __init__(self, calls_per_minute: int, calls_per_second: int):
        """Initialize rate limiter."""
        self.calls_per_minute = calls_per_minute
        self.calls_per_second = calls_per_second
        self.minute_calls = []
        self.second_calls = []
    
    async def acquire(self):
        """Acquire permission to make a request."""
        now = time.time()
        
        # Clean old timestamps
        self.minute_calls = [t for t in self.minute_calls if now - t < 60]
        self.second_calls = [t for t in self.second_calls if now - t < 1]
        
        # Check limits
        while len(self.minute_calls) >= self.calls_per_minute:
            await asyncio.sleep(0.1)
            now = time.time()
            self.minute_calls = [t for t in self.minute_calls if now - t < 60]
        
        while len(self.second_calls) >= self.calls_per_second:
            await asyncio.sleep(0.05)
            now = time.time()
            self.second_calls = [t for t in self.second_calls if now - t < 1]
        
        # Add new timestamp
        self.minute_calls.append(now)
        self.second_calls.append(now)


class ProbeResult:
    """Container for probe test results."""
    
    def __init__(
        self,
        test_name: str,
        success: bool,
        response: Dict[str, Any],
        duration: float,
        error: Optional[str] = None,
        notes: Optional[List[str]] = None,
        hypothesis_results: Optional[Dict[str, bool]] = None
    ):
        self.test_name = test_name
        self.success = success
        self.response = response
        self.duration = duration
        self.error = error
        self.notes = notes or []
        self.hypothesis_results = hypothesis_results or {}
        self.timestamp = datetime.now()
    
    def to_markdown(self) -> str:
        """Convert result to markdown format."""
        status = "✅" if self.success else "❌"
        md = [
            f"## {self.test_name} {status}",
            f"**Time**: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Duration**: {self.duration:.2f}s",
            "",
            "### Response",
            "```json",
            json.dumps(self.response, indent=2),
            "```",
            ""
        ]
        
        if self.error:
            md.extend([
                "### Error",
                f"```\n{self.error}\n```",
                ""
            ])
        
        if self.notes:
            md.extend([
                "### Notes",
                *[f"- {note}" for note in self.notes],
                ""
            ])
        
        if self.hypothesis_results:
            md.extend([
                "### Hypotheses Tested",
                *[f"- {h}: {'✅' if r else '❌'}" for h, r in self.hypothesis_results.items()],
                ""
            ])
        
        return "\n".join(md)


class APIProbe:
    """Main probe class for testing API endpoints."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.rate_limiter = RateLimiter(
            RATE_LIMIT_PER_MINUTE,
            RATE_LIMIT_PER_SECOND
        )
        self.results: List[ProbeResult] = []
    
    async def test_auth(self) -> ProbeResult:
        """Test authentication and rate limiting."""
        start = time.time()
        response = {"auth_test": "pending"}
        notes = []
        hypotheses = {
            "Auth uses Bearer token": False,
            "Rate limits are per endpoint": False,
            "Retry-After header present": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test with valid auth on inference endpoint
                await self.rate_limiter.acquire()
                async with session.post(
                    f"{BASE_URL}/inference/run",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model_id": "gpt_4o_mini_agent",
                        "llm_input": "test"
                    }
                ) as resp:
                    response["inference_auth"] = {
                        "status": resp.status,
                        "headers": dict(resp.headers)
                    }
                    if resp.status != 401:
                        notes.append("✅ Bearer auth works on inference")
                        hypotheses["Auth uses Bearer token"] = True
                
                # Test rate limiting on different endpoints
                endpoints = [
                    ("POST", "/inference/run", {"model_id": "gpt_4o_mini_agent", "llm_input": "test"}),
                    ("POST", "/contracts/score", {"contract": MINIMAL_CONTRACT, "llm_input": "test", "llm_output": "test"}),
                    ("POST", "/data/input/cluster", [{"identifier": "1", "llm_input": "test"}])
                ]
                
                rate_limits = {}
                for method, endpoint, data in endpoints:
                    requests = []
                    for _ in range(10):  # Try to hit rate limit
                        await self.rate_limiter.acquire()
                        requests.append(
                            session.request(
                                method,
                                f"{BASE_URL}{endpoint}",
                                headers={
                                    "Authorization": f"Bearer {self.api_key}",
                                    "Content-Type": "application/json"
                                },
                                json=data
                            )
                        )
                    
                    resps = await asyncio.gather(*requests, return_exceptions=True)
                    rate_limited = any(
                        getattr(r, 'status', 0) == 429 
                        for r in resps 
                        if not isinstance(r, Exception)
                    )
                    
                    if rate_limited:
                        rate_limits[endpoint] = True
                        retry_after = next(
                            (
                                r.headers.get("Retry-After")
                                for r in resps
                                if not isinstance(r, Exception) and r.status == 429
                            ),
                            None
                        )
                        if retry_after:
                            notes.append(f"✅ Retry-After header found on {endpoint}: {retry_after}")
                            hypotheses["Retry-After header present"] = True
                
                if len(set(rate_limits.values())) > 1:
                    notes.append("✅ Different endpoints have different rate limits")
                    hypotheses["Rate limits are per endpoint"] = True
            
            return ProbeResult(
                "Authentication & Rate Limits",
                True,
                response,
                time.time() - start,
                notes=notes,
                hypothesis_results=hypotheses
            )
        
        except Exception as e:
            return ProbeResult(
                "Authentication & Rate Limits",
                False,
                response,
                time.time() - start,
                str(e),
                notes,
                hypotheses
            )
    
    async def test_inference(self) -> ProbeResult:
        """Test inference endpoint behavior."""
        start = time.time()
        response = {"inference_test": "pending"}
        notes = []
        hypotheses = {
            "Inference is stateless": False,
            "Empty inputs rejected": False,
            "Long inputs handled": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test multiple inputs
                for input_text in SAMPLE_INPUTS:
                    await self.rate_limiter.acquire()
                    async with session.post(
                        f"{BASE_URL}/inference/run",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model_id": "gpt_4o_mini_agent",
                            "llm_input": input_text
                        }
                    ) as resp:
                        key = f"input_{len(input_text)}" if input_text else "empty_input"
                        response[key] = {
                            "status": resp.status,
                            "body": await resp.json() if resp.status == 200 else None,
                            "headers": dict(resp.headers)
                        }
                        
                        if not input_text and resp.status == 422:
                            notes.append("✅ Empty input correctly rejected")
                            hypotheses["Empty inputs rejected"] = True
                        
                        if len(input_text) > 500 and resp.status == 200:
                            notes.append("✅ Long input handled successfully")
                            hypotheses["Long inputs handled"] = True
                
                # Test statelessness
                same_input = "What is 2+2?"
                responses = []
                for _ in range(3):
                    await self.rate_limiter.acquire()
                    async with session.post(
                        f"{BASE_URL}/inference/run",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model_id": "gpt_4o_mini_agent",
                            "llm_input": same_input
                        }
                    ) as resp:
                        if resp.status == 200:
                            responses.append(await resp.json())
                
                # Check if responses are independent
                if len(responses) == 3:
                    texts = [r.get("text", "") for r in responses]
                    if len(set(texts)) == 3:
                        notes.append("✅ Same input produces different outputs - likely stateless")
                        hypotheses["Inference is stateless"] = True
            
            return ProbeResult(
                "Inference Behavior",
                True,
                response,
                time.time() - start,
                notes=notes,
                hypothesis_results=hypotheses
            )
        
        except Exception as e:
            return ProbeResult(
                "Inference Behavior",
                False,
                response,
                time.time() - start,
                str(e),
                notes,
                hypotheses
            )
    
    async def test_job_management(self) -> ProbeResult:
        """Test job management and streaming."""
        start = time.time()
        response = {"job_test": "pending"}
        notes = []
        hypotheses = {
            "Jobs use standard status codes": False,
            "Jobs support streaming": False,
            "Multiple jobs run in parallel": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Start a tuning job
                await self.rate_limiter.acquire()
                async with session.post(
                    f"{BASE_URL}/tune/prompt",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "contract": MINIMAL_CONTRACT,
                        "examples": [
                            {
                                "llm_input": "What is 2+2?",
                                "llm_output": "4"
                            }
                        ],
                        "model_id": "gpt-4o-mini",
                        "tuning_algorithm": "pi"
                    }
                ) as resp:
                    response["job_creation"] = {
                        "status": resp.status,
                        "body": await resp.json() if resp.status == 200 else None
                    }
                    
                    if resp.status == 200:
                        job_data = response["job_creation"]["body"]
                        job_id = job_data.get("job_id")
                        
                        if job_id:
                            # Test status endpoint
                            await self.rate_limiter.acquire()
                            async with session.get(
                                f"{BASE_URL}/tune/prompt/{job_id}",
                                headers={"Authorization": f"Bearer {self.api_key}"}
                            ) as status_resp:
                                response["job_status"] = {
                                    "status": status_resp.status,
                                    "body": await status_resp.json() if status_resp.status == 200 else None
                                }
                                
                                if status_resp.status == 200:
                                    status_data = response["job_status"]["body"]
                                    if "state" in status_data:
                                        notes.append("✅ Job status follows standard format")
                                        hypotheses["Jobs use standard status codes"] = True
                            
                            # Test streaming
                            await self.rate_limiter.acquire()
                            async with session.get(
                                f"{BASE_URL}/tune/prompt/{job_id}/messages",
                                headers={"Authorization": f"Bearer {self.api_key}"}
                            ) as stream_resp:
                                response["job_stream"] = {
                                    "status": stream_resp.status,
                                    "headers": dict(stream_resp.headers)
                                }
                                
                                if stream_resp.status == 200:
                                    content_type = stream_resp.headers.get("content-type", "")
                                    if "text/plain" in content_type:
                                        notes.append("✅ Streaming endpoint returns text/plain")
                                        hypotheses["Jobs support streaming"] = True
                
                # Test parallel jobs
                jobs = []
                for i in range(3):
                    await self.rate_limiter.acquire()
                    jobs.append(
                        session.post(
                            f"{BASE_URL}/tune/prompt",
                            headers={
                                "Authorization": f"Bearer {self.api_key}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "contract": MINIMAL_CONTRACT,
                                "examples": [
                                    {
                                        "llm_input": f"Test {i}",
                                        "llm_output": f"Output {i}"
                                    }
                                ],
                                "model_id": "gpt-4o-mini",
                                "tuning_algorithm": "pi"
                            }
                        )
                    )
                
                job_resps = await asyncio.gather(*jobs)
                if all(r.status == 200 for r in job_resps):
                    notes.append("✅ Multiple jobs accepted in parallel")
                    hypotheses["Multiple jobs run in parallel"] = True
            
            return ProbeResult(
                "Job Management",
                True,
                response,
                time.time() - start,
                notes=notes,
                hypothesis_results=hypotheses
            )
        
        except Exception as e:
            return ProbeResult(
                "Job Management",
                False,
                response,
                time.time() - start,
                str(e),
                notes,
                hypotheses
            )
    
    async def test_contract_dimensions(self) -> ProbeResult:
        """Test contract dimension generation and scoring."""
        start = time.time()
        response = {"dimension_test": "pending"}
        notes = []
        hypotheses = {
            "Dimensions are hierarchical": False,
            "Weights are normalized": False,
            "Generated dimensions are consistent": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Generate dimensions for similar contracts
                similar_contracts = [
                    {
                        "name": "math_test_1",
                        "description": "Test mathematical problem solving ability",
                        "dimensions": []
                    },
                    {
                        "name": "math_test_2",
                        "description": "Evaluate capability in solving math problems",
                        "dimensions": []
                    }
                ]
                
                dimension_sets = []
                for contract in similar_contracts:
                    await self.rate_limiter.acquire()
                    async with session.post(
                        f"{BASE_URL}/contracts/generate_dimensions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={"contract": contract}
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            dimension_sets.append(data.get("dimensions", []))
                
                response["dimension_generation"] = {
                    "contract_1": dimension_sets[0] if dimension_sets else None,
                    "contract_2": dimension_sets[1] if len(dimension_sets) > 1 else None
                }
                
                if dimension_sets:
                    # Check hierarchy
                    has_subdims = any(
                        d.get("sub_dimensions")
                        for dims in dimension_sets
                        for d in dims
                    )
                    if has_subdims:
                        notes.append("✅ Dimensions contain sub-dimensions")
                        hypotheses["Dimensions are hierarchical"] = True
                    
                    # Check weights
                    for dims in dimension_sets:
                        weights = [float(d.get("weight", 0)) for d in dims]
                        if weights and abs(sum(weights) - 1.0) < 0.001:
                            notes.append("✅ Dimension weights sum to 1.0")
                            hypotheses["Weights are normalized"] = True
                    
                    # Check consistency
                    if len(dimension_sets) > 1:
                        # Compare dimension labels
                        labels_1 = {d.get("label") for d in dimension_sets[0]}
                        labels_2 = {d.get("label") for d in dimension_sets[1]}
                        common = labels_1 & labels_2
                        if len(common) / max(len(labels_1), len(labels_2)) > 0.5:
                            notes.append("✅ Similar contracts generate similar dimensions")
                            hypotheses["Generated dimensions are consistent"] = True
            
            return ProbeResult(
                "Contract Dimensions",
                True,
                response,
                time.time() - start,
                notes=notes,
                hypothesis_results=hypotheses
            )
        
        except Exception as e:
            return ProbeResult(
                "Contract Dimensions",
                False,
                response,
                time.time() - start,
                str(e),
                notes,
                hypotheses
            )
    
    async def run_all_tests(self):
        """Run all probe tests in parallel."""
        tests = [
            self.test_auth(),
            self.test_inference(),
            self.test_job_management(),
            self.test_contract_dimensions()
        ]
        
        console.print(Panel("Running API Probe Tests", style="bold magenta"))
        results = await asyncio.gather(*tests)
        self.results.extend(results)
        
        # Print results
        table = Table(title="Test Results")
        table.add_column("Test", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Duration", style="magenta")
        table.add_column("Hypotheses", style="yellow")
        table.add_column("Notes", style="green")
        
        for result in results:
            status = "✅" if result.success else "❌"
            hypotheses = "\n".join(
                f"{h}: {'✅' if r else '❌'}"
                for h, r in result.hypothesis_results.items()
            )
            notes = "\n".join(result.notes) if result.notes else ""
            table.add_row(
                result.test_name,
                status,
                f"{result.duration:.2f}s",
                hypotheses,
                notes
            )
        
        console.print(table)
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save test results to markdown file."""
        output_path = Path(OUTPUT_FILE)
        
        content = [
            "# PI API Probe Results",
            f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            f"- Total Tests: {len(self.results)}",
            f"- Successful: {sum(1 for r in self.results if r.success)}",
            f"- Failed: {sum(1 for r in self.results if not r.success)}",
            "",
            "## Hypotheses Validation",
            ""
        ]
        
        # Aggregate hypothesis results
        all_hypotheses = {}
        for result in self.results:
            all_hypotheses.update(result.hypothesis_results)
        
        content.extend([
            "### Confirmed",
            *[f"- {h}" for h, r in all_hypotheses.items() if r],
            "",
            "### Rejected",
            *[f"- {h}" for h, r in all_hypotheses.items() if not r],
            "",
            "## Detailed Results",
            ""
        ])
        
        content.extend(result.to_markdown() for result in self.results)
        
        output_path.write_text("\n".join(content))
        console.print(f"\nResults saved to [bold cyan]{output_path}[/bold cyan]")


if __name__ == "__main__":
    # Load API key from environment
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("PI_API_KEY")
    
    if not api_key:
        console.print("[bold red]Error: PI_API_KEY environment variable not set[/bold red]")
        exit(1)
    
    # Run probe tests
    probe = APIProbe(api_key)
    asyncio.run(probe.run_all_tests())
