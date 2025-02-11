"""
PI SDK Probe - Test script for exploring PI SDK functionality.

This script provides:
1. SDK client usage examples
2. Contract and dimension testing
3. Tuning pattern exploration
4. Response analysis

Usage:
    python pi_sdk_probe.py --api-key YOUR_KEY

v5 - Fixed tuning patterns test and job ID handling
"""

import argparse
import asyncio
import concurrent.futures
import json
import logging
import signal
import sys
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Dict, Any, Callable

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel

from pi_sdk import PIClient

# Global configuration
RUN_IN_ASYNC = True  # Set to False for synchronous execution
API_KEY = "pilabs_key_epc8PlKUV7BzrsVJUJRzE3h3XLgxXa2zC6Hh7RSkIEo"
OUTPUT_DIR = Path("probe_results")
MAX_WORKERS = 5  # Maximum number of threads for parallel execution

# Console setup
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("pi_probe")

# Test data
TEST_INPUTS = [
    "What is 2+2?",
    "Explain quantum computing",
    "Write a haiku about AI"
]

TEST_CONTRACT = {
    "name": "Basic Test",
    "description": "Test basic functionality",
    "dimensions": [{
        "description": "Test accuracy",
        "label": "Accuracy",
        "sub_dimensions": [{
            "label": "Numerical",
            "description": "Test numerical accuracy",
            "scoring_type": "PI_SCORER"
        }]
    }]
}


def handle_interrupt(signum, frame):
    """Handle interrupt signal gracefully."""
    console.print("\n[yellow]Received interrupt signal. Cleaning up...[/yellow]")
    sys.exit(0)


def run_async(coro):
    """Run coroutine in event loop."""
    try:
        return asyncio.get_event_loop().run_until_complete(coro)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation interrupted by user.[/yellow]")
        return None
    except Exception as e:
        console.print(f"\n[red]Error running async operation: {str(e)}[/red]")
        return None


def thread_worker(func: Callable, *args, **kwargs):
    """Execute async function in a thread."""
    try:
        return run_async(func(*args, **kwargs))
    except Exception as e:
        console.print(f"\n[red]Error in thread worker: {str(e)}[/red]")
        return None


class SDKProbe:
    """Probe for exploring PI SDK functionality."""
    
    def __init__(self, api_key: str):
        """Initialize probe with SDK client."""
        self.client = PIClient(api_key=api_key)
        self.results = []
        OUTPUT_DIR.mkdir(exist_ok=True)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
    
    def save_result(self, name: str, data: Any):
        """Save test result to file."""
        if not data:
            console.print(f"[yellow]No data to save for {name}[/yellow]")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"{name}_{timestamp}.json"
        
        with output_file.open("w") as f:
            json.dump(data, f, indent=2)
        
        console.print(f"Results saved to [cyan]{output_file}[/cyan]")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()
    
    async def cleanup(self):
        """Clean up resources."""
        if hasattr(self.client, 'session') and self.client.session:
            await self.client.session.close()
        self.executor.shutdown(wait=True)
    
    async def _test_single_inference(self, client: PIClient, input_text: str) -> Dict:
        """Test inference for a single input."""
        try:
            # Test basic inference
            response = await client.inference.run(
                model_id="gpt_4o_mini_agent",
                llm_input=input_text
            )
            
            # Test with different parameters
            response_with_params = await client.inference.run(
                model_id="gpt_4o_mini_agent",
                llm_input=input_text,
                temperature=0.7,
                max_tokens=100
            )
            
            result = {
                "input": input_text,
                "basic_response": response,
                "parameterized_response": response_with_params
            }
            
            console.print(f"✅ Inference patterns tested: {input_text[:30]}...")
            return result
        
        except Exception as e:
            console.print(f"❌ Error: {str(e)}")
            return {
                "input": input_text,
                "error": str(e)
            }
    
    def test_inference_patterns(self) -> Dict:
        """Test inference patterns using SDK client."""
        if RUN_IN_ASYNC:
            return run_async(self._test_inference_patterns_async())
        
        results = []
        with self.executor as executor:
            futures = []
            for input_text in TEST_INPUTS:
                future = executor.submit(
                    thread_worker,
                    self._test_single_inference,
                    self.client,
                    input_text
                )
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        
        return {"inference_patterns": results}
    
    async def _test_inference_patterns_async(self) -> Dict:
        """Async version of inference pattern testing."""
        results = []
        async with self.client as client:
            tasks = [
                self._test_single_inference(client, input_text)
                for input_text in TEST_INPUTS
            ]
            results = await asyncio.gather(*tasks)
        
        return {"inference_patterns": results}
    
    async def _test_single_contract(self, client: PIClient, input_text: str, dimensions: Dict) -> Dict:
        """Test contract scoring for a single input."""
        try:
            score = await client.contracts.score(
                contract=dimensions,
                llm_input=input_text,
                llm_output="Test output"
            )
            
            result = {
                "input": input_text,
                "dimensions": dimensions,
                "score": score
            }
            
            console.print(f"✅ Contract patterns tested: {input_text[:30]}...")
            return result
        
        except Exception as e:
            console.print(f"❌ Error: {str(e)}")
            return {
                "input": input_text,
                "error": str(e)
            }
    
    def test_contract_patterns(self) -> Dict:
        """Test contract patterns using SDK client."""
        if RUN_IN_ASYNC:
            return run_async(self._test_contract_patterns_async())
        
        results = []
        try:
            # Generate dimensions first
            dimensions = run_async(self._generate_dimensions())
            
            # Test scoring in parallel
            with self.executor as executor:
                futures = []
                for input_text in TEST_INPUTS:
                    future = executor.submit(
                        thread_worker,
                        self._test_single_contract,
                        self.client,
                        input_text,
                        dimensions
                    )
                    futures.append(future)
                
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
        
        except Exception as e:
            console.print(f"❌ Error: {str(e)}")
            results.append({"error": str(e)})
        
        return {"contract_patterns": results}
    
    async def _generate_dimensions(self) -> Dict:
        """Generate dimensions for contract testing."""
        async with self.client as client:
            return await client.contracts.generate_dimensions(
                name="Test Contract",
                description="A test contract for exploring patterns"
            )
    
    async def _test_contract_patterns_async(self) -> Dict:
        """Async version of contract pattern testing."""
        results = []
        async with self.client as client:
            try:
                dimensions = await self._generate_dimensions()
                tasks = [
                    self._test_single_contract(client, input_text, dimensions)
                    for input_text in TEST_INPUTS
                ]
                results = await asyncio.gather(*tasks)
            
            except Exception as e:
                console.print(f"❌ Error: {str(e)}")
                results.append({"error": str(e)})
        
        return {"contract_patterns": results}
    
    def test_tuning_patterns(self) -> Dict:
        """Test tuning patterns using SDK client."""
        if RUN_IN_ASYNC:
            return run_async(self._test_tuning_patterns_async())
        
        return run_async(self._test_tuning_patterns_async())  # Tuning is inherently async due to streaming
    
    async def _test_tuning_patterns_async(self) -> Dict:
        """Async version of tuning pattern testing."""
        results = []
        async with self.client as client:
            try:
                # Start tuning job
                job = await client.tune.start_prompt(
                    contract=TEST_CONTRACT,
                    examples=[
                        {"llm_input": "What is 2+2?", "llm_output": "4"},
                        {"llm_input": "What is 3+3?", "llm_output": "6"},
                        {"llm_input": "What is 5+5?", "llm_output": "10"}
                    ],
                    model_id="gpt-4o-mini"
                )
                
                # Extract job ID from response
                job_id = None
                if isinstance(job, dict):
                    job_id = job.get("job_id") or job.get("id")
                elif hasattr(job, "job_id"):
                    job_id = job.job_id
                elif hasattr(job, "id"):
                    job_id = job.id
                
                if not job_id:
                    raise ValueError(f"No job ID found in tuning response: {job}")
                
                # Stream tuning messages
                messages = []
                async for msg in client.tune.stream_messages(job_id):
                    messages.append(msg)
                    console.print(f"📝 Tuning message: {msg}")
                
                # Get final status
                final_status = await client.tune.get_status(job_id)
                
                results.append({
                    "job_id": job_id,
                    "messages": messages,
                    "final_status": final_status
                })
                
                console.print("✅ Tuning patterns tested")
            
            except Exception as e:
                console.print(f"❌ Error in tuning patterns: {str(e)}")
                results.append({
                    "error": str(e),
                    "job_response": job if "job" in locals() else None
                })
        
        return {"tuning_patterns": results}
    
    async def run_all_tests_async(self):
        """Run all probe tests asynchronously."""
        try:
            console.print("\n[bold magenta]Running PI SDK Probe Tests[/bold magenta]\n")
            
            # Test inference patterns
            console.print(Panel("Testing Inference Patterns", style="blue"))
            inference_results = await self._test_inference_patterns_async()
            self.save_result("inference_patterns", inference_results)
            
            # Test contract patterns
            console.print(Panel("Testing Contract Patterns", style="blue"))
            contract_results = await self._test_contract_patterns_async()
            self.save_result("contract_patterns", contract_results)
            
            # Test tuning patterns
            console.print(Panel("Testing Tuning Patterns", style="blue"))
            tuning_results = await self._test_tuning_patterns_async()
            self.save_result("tuning_patterns", tuning_results)
            
            console.print("\n[bold green]All tests completed![/bold green]")
        finally:
            await self.cleanup()
    
    def run_all_tests(self):
        """Run all probe tests."""
        if RUN_IN_ASYNC:
            asyncio.run(self.run_all_tests_async())
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.run_all_tests_async())
            finally:
                loop.close()


def main():
    """Main entry point."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)
    
    parser = argparse.ArgumentParser(description="PI SDK Probe")
    parser.add_argument("--api-key", default=API_KEY, help="PI API key")
    parser.add_argument("--sync", action="store_true", help="Run in synchronous mode")
    args = parser.parse_args()
    
    if args.sync:
        global RUN_IN_ASYNC
        RUN_IN_ASYNC = False
    
    try:
        probe = SDKProbe(args.api_key)
        probe.run_all_tests()
    except KeyboardInterrupt:
        console.print("\n[yellow]Probe execution interrupted by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error running probe: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main() 