"""
Jian Prompt Executor - SDK Implementation

This module demonstrates executing the Jian prompt using Vellum's SDK.

1. Initialize Vellum client
2. Execute prompt with inputs
3. Handle response and errors
v1
"""

import os
from vellum.client import Vellum
from dotenv import load_dotenv
from rich.console import Console

console = Console()

def execute_jian_prompt(input_text: str, stream: bool = False):
    """
    1. Load credentials
    2. Initialize client
    3. Execute prompt
    4. Return results
    v1
    """
    try:
        # Load environment variables
        load_dotenv()
        api_key = os.getenv('VELLUM_API_KEY')
        
        if not api_key:
            raise ValueError("No API key found. Set VELLUM_API_KEY in .env")

        # Initialize client
        client = Vellum(api_key=api_key)
        
        # Prepare inputs
        inputs = [
            {
                "name": "user_input",
                "value": input_text
            }
        ]
        
        # Execute prompt
        if stream:
            return stream_response(client, inputs)
        else:
            response = client.execute_prompt(
                prompt_deployment_name="jian",
                inputs=inputs
            )
            
            if response.state == "REJECTED":
                raise Exception(f"Prompt execution rejected: {response.error.message if hasattr(response, 'error') else 'Unknown error'}")
                
            return response.outputs[0].value if response.outputs else None
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return None

async def stream_response(client, inputs):
    """
    1. Stream response chunks
    2. Print as received
    3. Handle errors
    v1
    """
    try:
        async for chunk in client.execute_prompt_stream(
            prompt_deployment_name="jian",
            inputs=inputs
        ):
            if chunk.state == "REJECTED":
                raise Exception(f"Stream rejected: {chunk.error.message if hasattr(chunk, 'error') else 'Unknown error'}")
            
            if hasattr(chunk, 'outputs') and chunk.outputs:
                for output in chunk.outputs:
                    if hasattr(output, 'value'):
                        print(output.value, end="", flush=True)
        
        print()  # Final newline
        return True
        
    except Exception as e:
        console.print(f"\n[red]Streaming error: {str(e)}[/red]")
        return False

if __name__ == "__main__":
    # Demo execution
    console.print("\n[bold cyan]Jian Prompt Executor Demo[/bold cyan]")
    console.print("This demo shows both regular and streaming execution.\n")
    
    test_input = "Tell me about the importance of clear code documentation"
    
    # Regular execution
    console.print("\n[yellow]Regular Execution:[/yellow]")
    result = execute_jian_prompt(test_input)
    if result:
        console.print(f"\n[green]Response:[/green]\n{result}")
    
    # Streaming execution
    console.print("\n[yellow]Streaming Execution:[/yellow]")
    import asyncio
    asyncio.run(stream_response(Vellum(os.getenv('VELLUM_API_KEY')), [{"name": "user_input", "value": test_input}])) 