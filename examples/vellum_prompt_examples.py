"""
Vellum Prompt Examples - Demonstrates different ways to call Vellum prompts.

This module provides examples of:
1. Using Python SDK for prompt execution - [Simple, recommended approach]
2. Using HTTP requests directly - [For environments without SDK support]
3. Error handling and retries - [Best practices for production use]
4. Export functionality - [CSV/XLSX/JSON support]

Run this file directly to see a demo of all functionality.
v3 - Aligned with CLI implementation
"""

import json
import os
import time
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import vellum.types as types
from dotenv import load_dotenv
from rich.console import Console
from vellum.client import Vellum

# -------------------- 1. CONFIGURATION -------------------------------
# Global configuration
VELLUM_API_KEY = os.getenv('VELLUM_API_KEY')
BASE_URL = "https://predict.vellum.ai/v1"
EXAMPLE_PROMPT_NAME = "translate-anything-into-english"  # A real prompt from our workspace
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

console = Console()


# -------------------- 2. PYTHON SDK IMPLEMENTATION ------------------
class VellumSDKExample:
    """Example implementation using Vellum's Python SDK."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        1. Initialize with API key
        2. Set up Vellum client
        3. Configure console output
        v3 - Added error handling
        """
        self.api_key = api_key or VELLUM_API_KEY
        if not self.api_key:
            raise ValueError("No API key provided. Set VELLUM_API_KEY in .env or pass directly.")
        
        self.client = Vellum(api_key=self.api_key)
        self.console = Console()
    
    def execute_prompt(self, inputs: Dict[str, str]) -> Any:
        """
        1. Prepare inputs for Vellum format
        2. Execute prompt with retry logic
        3. Handle response and errors
        v3 - Improved error handling
        """
        # Convert inputs to Vellum format
        vellum_inputs = [
            types.PromptRequestStringInput(
                name=name,
                key=name,  # Use name as key
                value=value
            )
            for name, value in inputs.items()
        ]
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.execute_prompt(
                    prompt_deployment_name=EXAMPLE_PROMPT_NAME,
                    inputs=vellum_inputs
                )
                
                if response.state == "REJECTED":
                    error_msg = response.error.message if hasattr(response, 'error') else "Unknown error"
                    raise Exception(f"Prompt execution rejected: {error_msg}")
                
                return response.outputs[0].value if response.outputs else None
                
            except Exception:
                if attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(RETRY_DELAY * (2 ** attempt))  # Exponential backoff


# -------------------- 3. HTTP IMPLEMENTATION -----------------------
class VellumHTTPExample:
    """Example implementation using direct HTTP requests."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        1. Initialize with API key
        2. Set up HTTP headers
        3. Configure base URL
        v3 - Added error handling
        """
        self.api_key = api_key or VELLUM_API_KEY
        if not self.api_key:
            raise ValueError("No API key provided. Set VELLUM_API_KEY in .env or pass directly.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.base_url = BASE_URL
        self.console = Console()
    
    def execute_prompt(self, inputs: Dict[str, str]) -> Any:
        """
        1. Prepare request payload
        2. Send HTTP request
        3. Handle response and errors
        v3 - Improved error handling
        """
        # Prepare payload
        payload = {
            "prompt_deployment_name": EXAMPLE_PROMPT_NAME,
            "inputs": [
                {
                    "name": name,
                    "key": name,
                    "value": value
                }
                for name, value in inputs.items()
            ]
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    f"{self.base_url}/execute-prompt",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get("state") == "REJECTED":
                    raise Exception(f"Prompt execution rejected: {result.get('error', {}).get('message', 'Unknown error')}")
                
                return result.get("outputs", [{}])[0].get("value")
                
            except Exception:
                if attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(RETRY_DELAY * (2 ** attempt))  # Exponential backoff


# -------------------- 4. EXPORT FUNCTIONALITY -----------------------
def export_data(data: List[Dict], filepath: str) -> bool:
    """
    Export data to file in various formats.

    1. Determine format from extension
    2. Convert data to appropriate format
    3. Save to file
    v1 - Initial implementation
    """
    try:
        # Get file extension
        _, ext = os.path.splitext(filepath)
        ext = ext.lower()

        # Convert data based on format
        if ext == '.csv':
            if not data:
                return False
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        elif ext == '.xlsx':
            if not data:
                return False
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False)
        elif ext == '.json':
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        return True

    except Exception as e:
        print(f"Error exporting data: {str(e)}")
        return False


# -------------------- 5. DEMO FUNCTIONALITY -----------------------
def demo_functionality():
    """
    Run a demonstration of different Vellum prompt execution methods.
    
    1. Show SDK examples
    2. Show HTTP examples
    3. Demonstrate error handling
    4. Show export functionality
    v4 - Updated to use real prompt example
    """
    console = Console()
    
    # Load environment variables
    load_dotenv()
    
    # Validate API key
    if not VELLUM_API_KEY:
        console.print("[red]Error: VELLUM_API_KEY not found in environment variables[/red]")
        console.print("Please create a .env file with your Vellum API key:")
        console.print("VELLUM_API_KEY=your-api-key-here")
        return
    
    # Example inputs for translation prompt
    example_inputs = {
        "text": "Bonjour le monde! Comment allez-vous?",  # French text to translate
        "source_language": "French",
        "target_language": "English"
    }
    
    console.print("\n[bold cyan]Vellum Prompt Execution Examples[/bold cyan]")
    console.print("\nThis demo shows different ways to execute Vellum prompts.")
    console.print("Using API key from .env file.")
    
    # Print configuration
    console.print("\n[bold yellow]Configuration:[/bold yellow]")
    console.print(f"API Base URL: {BASE_URL}")
    console.print(f"Example Prompt: {EXAMPLE_PROMPT_NAME}")
    console.print(f"Max Retries: {MAX_RETRIES}")
    console.print(f"Retry Delay: {RETRY_DELAY} seconds")
    
    # Print example inputs
    console.print("\n[bold yellow]Example Inputs:[/bold yellow]")
    console.print("Text to translate: [cyan]" + example_inputs["text"] + "[/cyan]")
    console.print(f"From: [green]{example_inputs['source_language']}[/green]")
    console.print(f"To: [green]{example_inputs['target_language']}[/green]")
    
    # 1. SDK Example
    console.print("\n[bold]1. Using Python SDK[/bold]")
    try:
        sdk_client = VellumSDKExample()
        console.print("[cyan]Executing prompt...[/cyan]")
        result = sdk_client.execute_prompt(example_inputs)
        console.print(f"[green]Result:[/green] {result}")
        
        # Export result
        if result:
            export_data([{"output": result}], "sdk_result.json")
            console.print("[green]Result exported to sdk_result.json[/green]")
            
    except ValueError as e:
        console.print(f"[red]Configuration Error: {str(e)}[/red]")
        console.print("[yellow]Tip: Make sure your API key is set in .env file[/yellow]")
    except Exception as e:
        console.print(f"[red]SDK Error: {str(e)}[/red]")
        console.print("[yellow]Tip: Check if the prompt name exists and is accessible[/yellow]")
    
    # 2. HTTP Example
    console.print("\n[bold]2. Using HTTP Requests[/bold]")
    try:
        http_client = VellumHTTPExample()
        console.print("[cyan]Sending HTTP request...[/cyan]")
        result = http_client.execute_prompt(example_inputs)
        console.print(f"[green]Result:[/green] {result}")
        
        # Export result
        if result:
            export_data([{"output": result}], "http_result.json")
            console.print("[green]Result exported to http_result.json[/green]")
            
    except ValueError as e:
        console.print(f"[red]Configuration Error: {str(e)}[/red]")
        console.print("[yellow]Tip: Make sure your API key is set in .env file[/yellow]")
    except Exception as e:
        console.print(f"[red]HTTP Error: {str(e)}[/red]")
        console.print("[yellow]Tip: Check your network connection and API endpoint[/yellow]")
    
    # Summary
    console.print("\n[bold yellow]Demo Complete![/bold yellow]")
    console.print("For more examples and documentation, check the README.md")


if __name__ == "__main__":
    demo_functionality() 