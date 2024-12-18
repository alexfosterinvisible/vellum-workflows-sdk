"""
Jian Prompt Executor - HTTP Implementation

This module demonstrates executing the Jian prompt using direct HTTP calls.

1. Make HTTP requests to Vellum API
2. Handle streaming and non-streaming responses
3. Process results
v1
"""

import os
import requests
import json
from dotenv import load_dotenv
from rich.console import Console
import sseclient

console = Console()

class JianPromptHTTP:
    """
    1. Handle HTTP requests to Vellum API
    2. Support both streaming and regular execution
    3. Process responses
    v1
    """
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('VELLUM_API_KEY')
        if not self.api_key:
            raise ValueError("No API key found. Set VELLUM_API_KEY in .env")
        
        self.base_url = "https://predict.vellum.ai/v1"
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    def execute(self, input_text: str, stream: bool = False):
        """
        1. Prepare request
        2. Execute prompt
        3. Handle response
        v1
        """
        endpoint = f"{self.base_url}/execute-prompt{'-stream' if stream else ''}"
        
        payload = {
            "prompt_deployment_name": "jian",
            "inputs": [
                {
                    "name": "user_input",
                    "value": input_text
                }
            ]
        }
        
        try:
            if stream:
                return self._handle_stream(endpoint, payload)
            else:
                response = requests.post(endpoint, headers=self.headers, json=payload)
                response.raise_for_status()
                result = response.json()
                
                if result.get("state") == "REJECTED":
                    raise Exception(f"Prompt execution rejected: {result.get('error', {}).get('message', 'Unknown error')}")
                
                return result.get("outputs", [{}])[0].get("value")
                
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            return None

    def _handle_stream(self, endpoint: str, payload: dict):
        """
        1. Handle SSE stream
        2. Process chunks
        3. Return results
        v1
        """
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload, stream=True)
            response.raise_for_status()
            
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.data:
                    data = json.loads(event.data)
                    if data.get("type") == "STREAMING":
                        print(data.get("delta", ""), end="", flush=True)
                    elif data.get("type") == "FULFILLED":
                        print()  # Final newline
                        return True
                    elif data.get("state") == "REJECTED":
                        raise Exception(f"Stream rejected: {data.get('error', {}).get('message', 'Unknown error')}")
            
            return True
            
        except Exception as e:
            console.print(f"\n[red]Streaming error: {str(e)}[/red]")
            return False

if __name__ == "__main__":
    # Demo execution
    console.print("\n[bold cyan]Jian Prompt Executor (HTTP) Demo[/bold cyan]")
    console.print("This demo shows both regular and streaming execution.\n")
    
    jian = JianPromptHTTP()
    test_input = "Tell me about the importance of clear code documentation"
    
    # Regular execution
    console.print("\n[yellow]Regular Execution:[/yellow]")
    result = jian.execute(test_input)
    if result:
        console.print(f"\n[green]Response:[/green]\n{result}")
    
    # Streaming execution
    console.print("\n[yellow]Streaming Execution:[/yellow]")
    jian.execute(test_input, stream=True) 