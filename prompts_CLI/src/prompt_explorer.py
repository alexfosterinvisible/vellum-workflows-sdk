"""
Vellum Prompt CLI - CLI helper for LLMS to explore and execute Vellum prompts, and diagnose issues.

This module provides functionality to:
1. List available prompts - [via deployments.list endpoint, use: vellum-explorer list --status ACTIVE] - [90% complete, TODO: Add filtering by environment]
2. View prompt details - [via deployments.get endpoint, use: vellum-explorer show <prompt-name>] - [80% complete, TODO: Add version history, usage stats]
3. Execute prompts with custom inputs - [via execute_prompt endpoint, use: vellum-explorer execute <prompt-name> --inputs '{"key": "value"}'] - [95% complete, TODO: Add streaming support]
4. Save and manage prompt results - [Export to CSV/XLSX/JSON] - [100% complete]
5. Help / Code Diagnostic based on learnings - TODO: Integrate with learnings documentation for automated troubleshooting

v6 - Added export functionality
"""

import os
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import csv
import json
import pandas as pd

from vellum.client import Vellum
import vellum.types as types
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table


# -------------------- 1. LIST AVAILABLE PROMPTS -------------------------------
@dataclass
class PromptInfo:
    """Information about a Vellum prompt deployment."""
    id: str
    name: str
    label: str
    created: datetime
    last_deployed: datetime
    status: str
    environment: str
    description: Optional[str] = None


# -------------------- 2. CORE FUNCTIONALITY & INITIALIZATION ----------------
class PromptExplorer:
    """Main class for interacting with Vellum prompts."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the PromptExplorer.

        1. Load environment variables
        2. Initialize Vellum client
        3. Set up rich console for output
        v2 - Added result caching
        """
        # Load environment variables if no API key provided
        if not api_key:
            load_dotenv()
            api_key = os.getenv('VELLUM_API_KEY')

        if not api_key:
            raise ValueError("No API key provided. Set VELLUM_API_KEY in .env or pass directly.")

        # Initialize Vellum client and cache
        self.client = Vellum(api_key=api_key)
        self.console = Console()
        self._cache = {}

    def export_prompts(self, filepath: str) -> bool:
        """
        Export prompt list to file.

        1. Get all prompts
        2. Convert to exportable format
        3. Save to file
        v1 - Initial implementation
        """
        prompts = self.list_prompts()
        if not prompts:
            return False

        # Convert prompts to dict format
        prompt_data = [
            {
                "id": p.id,
                "name": p.name,
                "label": p.label,
                "created": p.created,
                "last_deployed": p.last_deployed,
                "status": p.status,
                "environment": p.environment,
                "description": p.description
            }
            for p in prompts
        ]

        return export_data(prompt_data, filepath)

    def export_execution_result(self, result: Dict[str, Any], filepath: str) -> bool:
        """
        Export execution result to file.

        1. Convert result to exportable format
        2. Save to file
        v1 - Initial implementation
        """
        if not result:
            return False

        # Convert result to list format for export
        result_data = []
        for item in result:
            if hasattr(item, 'value'):
                result_data.append({"output": item.value})
            else:
                result_data.append({"output": str(item)})

        return export_data(result_data, filepath)

    def list_prompts(self, status: str = "ACTIVE", environment: Optional[str] = None) -> List[PromptInfo]:
        """
        List all available prompts.

        1. Call Vellum API to get prompts
        2. Convert to PromptInfo objects
        3. Filter by environment if specified
        4. Return sorted list by creation date
        v2 - Added environment filtering
        """
        try:
            # Get deployments from Vellum
            response = self.client.deployments.list(status=status)

            # Convert to PromptInfo objects
            prompts = []
            for deployment in response.results:
                # Skip if environment doesn't match
                if environment and deployment.environment != environment:
                    continue
                    
                prompt = PromptInfo(
                    id=deployment.id,
                    name=deployment.name,
                    label=deployment.label,
                    created=deployment.created,
                    last_deployed=deployment.last_deployed_on,
                    status=deployment.status,
                    environment=deployment.environment,
                    description=deployment.description
                )
                prompts.append(prompt)

            # Sort by creation date
            return sorted(prompts, key=lambda x: x.created, reverse=True)

        except Exception as e:
            self.console.print(f"[red]Error listing prompts: {str(e)}[/red]")
            return []

    def get_prompt_details(self, prompt_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific prompt.

        1. Get deployment details from Vellum
        2. Get version history
        3. Format details for display
        4. Cache results for future use
        v2 - Updated to use list and filter instead of direct get
        """
        cache_key = f"details_{prompt_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            # Get deployment details from list
            response = self.client.deployments.list()
            deployment = next(
                (d for d in response.results if d.name == prompt_name),
                None
            )
            
            if not deployment:
                return None
            
            # Get version history (if available)
            versions = []
            try:
                history = self.client.deployments.list_versions(prompt_name)
                versions = [
                    {
                        "version": v.version,
                        "created": v.created,
                        "status": v.status
                    }
                    for v in history.results
                ]
            except:
                pass  # Version history is optional

            # Format details
            details = {
                "id": deployment.id,
                "name": deployment.name,
                "label": deployment.label,
                "description": deployment.description,
                "environment": deployment.environment,
                "status": deployment.status,
                "created": deployment.created,
                "last_deployed": deployment.last_deployed_on,
                "versions": versions,
                "input_variables": deployment.input_variables if hasattr(deployment, 'input_variables') else [],
                "model": deployment.model if hasattr(deployment, 'model') else "Unknown"
            }

            # Cache results
            self._cache[cache_key] = details
            return details

        except Exception as e:
            self.console.print(f"[red]Error getting prompt details: {str(e)}[/red]")
            return None

    def display_prompt_details(self, details: Dict[str, Any]) -> None:
        """
        Display detailed prompt information in a formatted way.

        1. Create sections for different types of information
        2. Format version history if available
        3. Display required inputs
        v2 - Fixed console reference
        """
        if not details:
            return

        # Basic Information
        self.console.print("\n[bold cyan]Prompt Details[/bold cyan]")
        self.console.print(f"Name: [green]{details['name']}[/green]")
        self.console.print(f"Label: [yellow]{details['label']}[/yellow]")
        if details['description']:
            self.console.print(f"Description: {details['description']}")
        self.console.print(f"Environment: [blue]{details['environment']}[/blue]")
        self.console.print(f"Status: [magenta]{details['status']}[/magenta]")
        self.console.print(f"Model: [cyan]{details['model']}[/cyan]")

        # Dates
        self.console.print("\n[bold cyan]Timestamps[/bold cyan]")
        self.console.print(f"Created: {details['created'].strftime('%Y-%m-%d %H:%M:%S')}")
        self.console.print(f"Last Deployed: {details['last_deployed'].strftime('%Y-%m-%d %H:%M:%S')}")

        # Input Variables
        if details['input_variables']:
            self.console.print("\n[bold cyan]Required Input Variables[/bold cyan]")
            for var in details['input_variables']:
                self.console.print(f"- [yellow]{var}[/yellow]")

        # Version History
        if details['versions']:
            self.console.print("\n[bold cyan]Version History[/bold cyan]")
            table = Table()
            table.add_column("Version")
            table.add_column("Created")
            table.add_column("Status")

            for version in details['versions']:
                table.add_row(
                    str(version['version']),
                    version['created'].strftime('%Y-%m-%d %H:%M:%S'),
                    version['status']
                )
            self.console.print(table)

    def display_prompts(self, prompts: List[PromptInfo]) -> None:
        """
        Display prompts in a formatted table.

        1. Create rich table
        2. Add prompt information
        3. Print to console
        v1
        """
        table = Table(title="Available Vellum Prompts")

        # Add columns
        table.add_column("Name", style="cyan")
        table.add_column("Label", style="magenta")
        table.add_column("Environment", style="green")
        table.add_column("Last Deployed", style="yellow")
        table.add_column("Status", style="blue")

        # Add rows
        for prompt in prompts:
            table.add_row(
                prompt.name,
                prompt.label,
                prompt.environment,
                prompt.last_deployed.strftime("%Y-%m-%-d %H:%M:%S"),
                prompt.status
            )

        self.console.print(table)


# -------------------- 4. PROMPT EXECUTION ---------------------------------

    def execute_prompt(
        self, 
        prompt_name: str, 
        inputs: Dict[str, str], 
        release_tag: str = "LATEST",
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a prompt with the given inputs.

        1. Convert inputs to Vellum format
        2. Execute prompt (streaming or regular)
        3. Handle errors and return results
        4. Format streaming output if enabled
        v5 - Fixed streaming output to use print for real-time display
        """
        try:
            # Convert inputs to Vellum format
            vellum_inputs = [
                types.PromptRequestStringInput(
                    name=name,
                    key="",
                    value=value
                )
                for name, value in inputs.items()
            ]

            if stream:
                # Execute prompt with streaming
                try:
                    self.console.print("[cyan]Starting streaming output...[/cyan]")
                    for chunk in self.client.execute_prompt_stream(
                        prompt_deployment_name=prompt_name,
                        release_tag=release_tag,
                        inputs=vellum_inputs
                    ):
                        if chunk.state == "REJECTED":
                            error_msg = chunk.error.message if hasattr(chunk, 'error') else "Unknown error"
                            self.console.print(f"[red]Error executing prompt: {error_msg}[/red]")
                            return {}
                        
                        # Print each chunk as it arrives
                        if hasattr(chunk, 'outputs') and chunk.outputs:
                            for output in chunk.outputs:
                                if hasattr(output, 'value'):
                                    print(output.value, end="", flush=True)
                    
                    print()  # Final newline
                    self.console.print("[green]Streaming complete![/green]")
                    return {"status": "success", "message": "Streaming complete"}
                
                except Exception as e:
                    self.console.print(f"\n[red]Error during streaming: {str(e)}[/red]")
                    return {}
            else:
                # Execute prompt normally
                result = self.client.execute_prompt(
                    prompt_deployment_name=prompt_name,
                    release_tag=release_tag,
                    inputs=vellum_inputs
                )

                # Check for errors
                if result.state == "REJECTED":
                    error_msg = result.error.message if hasattr(result, 'error') else "Unknown error"
                    self.console.print(f"[red]Error executing prompt: {error_msg}[/red]")
                    return {}

                return result.outputs

        except Exception as e:
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                error_detail = e.response.json().get('detail', str(e))
                if "Input variable" in error_detail and "not found" in error_detail:
                    var_name = error_detail.split("'")[1]
                    self.console.print(f"[yellow]Missing required input variable: {var_name}[/yellow]")
                    self.console.print(f"[yellow]Use 'vellum-explorer show {prompt_name}' to see all required variables[/yellow]")
                else:
                    self.console.print(f"[red]Error: {error_detail}[/red]")
            else:
                self.console.print(f"[red]Error: {str(e)}[/red]")
            return {}


# -------------------- 6. EXPORT FUNCTIONALITY -------------------------------
def export_data(data: List[Dict], filepath: str) -> bool:
    """
    Export data to file in various formats.

    1. Determine format from extension
    2. Convert data to appropriate format
    3. Save to file
    4. Handle export errors
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


# -------------------- 7. LEARNINGS INTEGRATION -------------------------------
def get_learning_by_error(error_message: str) -> Optional[str]:
    """
    Get relevant learning based on error message.

    1. Match error pattern
    2. Return relevant guidance
    3. Provide example if available
    v1 - Initial implementation
    """
    error_patterns = {
        "Input variable": (
            "Missing required input variable. Use 'show' command to see required variables:\n"
            "vellum-explorer show <prompt-name>"
        ),
        "Invalid API key": (
            "API key validation failed. Check:\n"
            "1. VELLUM_API_KEY in .env file\n"
            "2. API key permissions\n"
            "3. Environment variables are loaded"
        ),
        "rate limit": (
            "Rate limit reached. Consider:\n"
            "1. Implementing exponential backoff\n"
            "2. Tracking API usage\n"
            "3. Queuing requests when near limits"
        ),
        "not found": (
            "Resource not found. Note:\n"
            "1. Vellum client lacks direct 'get' method\n"
            "2. Use list() and filter instead\n"
            "3. Check environment and status filters"
        )
    }

    for pattern, guidance in error_patterns.items():
        if pattern.lower() in error_message.lower():
            return guidance
    
    return None


def get_learning_by_topic(topic: str) -> Optional[str]:
    """
    Get learning guidance by topic.

    1. Match topic
    2. Return relevant guidance
    3. Provide examples
    v1 - Initial implementation
    """
    topics = {
        "streaming": (
            "Streaming Output Tips:\n"
            "1. Use --stream flag for real-time output\n"
            "2. Note: Streaming disables Rich formatting\n"
            "3. Example: vellum-explorer execute my-prompt --inputs '{...}' --stream"
        ),
        "export": (
            "Export Functionality:\n"
            "1. Supported formats: csv, xlsx, json\n"
            "2. Use --export flag with desired filename\n"
            "3. Examples:\n"
            "   - List: vellum-explorer list --export prompts.csv\n"
            "   - Execute: vellum-explorer execute my-prompt --inputs '{...}' --export results.xlsx"
        ),
        "environment": (
            "Environment Management:\n"
            "1. Filter by environment: --environment DEVELOPMENT\n"
            "2. Set API key in .env file\n"
            "3. Example: vellum-explorer list --environment PRODUCTION"
        ),
        "input": (
            "Input Handling:\n"
            "1. Use JSON format for inputs\n"
            "2. Check required variables with 'show' command\n"
            "3. Example: vellum-explorer execute my-prompt --inputs '{\"var\": \"value\"}'"
        )
    }

    return topics.get(topic.lower())


class PromptExplorer:
    def get_help(self, topic: Optional[str] = None, error: Optional[str] = None) -> None:
        """
        Get help and guidance based on topic or error.

        1. Check for error-specific guidance
        2. Check for topic-specific guidance
        3. Display relevant information
        v1 - Initial implementation
        """
        if error:
            guidance = get_learning_by_error(error)
            if guidance:
                self.console.print("\n[bold cyan]Error Guidance:[/bold cyan]")
                self.console.print(guidance)
                return

        if topic:
            guidance = get_learning_by_topic(topic)
            if guidance:
                self.console.print("\n[bold cyan]Topic Guidance:[/bold cyan]")
                self.console.print(guidance)
                return

        # Default help if no specific guidance found
        self.console.print("\n[bold cyan]Available Help Topics:[/bold cyan]")
        self.console.print("1. streaming - Real-time output handling")
        self.console.print("2. export - Data export functionality")
        self.console.print("3. environment - Environment management")
        self.console.print("4. input - Input handling and validation")
        self.console.print("\nUse: vellum-explorer help <topic>")

    def handle_error(self, error: str, context: Optional[str] = None) -> None:
        """
        Handle errors with guidance from learnings.

        1. Display error message
        2. Get relevant guidance
        3. Show context-specific help
        v1 - Initial implementation
        """
        self.console.print(f"[red]Error: {error}[/red]")
        
        # Get guidance
        guidance = get_learning_by_error(error)
        if guidance:
            self.console.print("\n[yellow]Suggested Solution:[/yellow]")
            self.console.print(guidance)
        
        # Show context help
        if context:
            topic_help = get_learning_by_topic(context)
            if topic_help:
                self.console.print("\n[yellow]Related Information:[/yellow]")
                self.console.print(topic_help)


# -------------------- 5. MAIN EXECUTION ----------------------------------
def demo_functionality():
    """Run a demonstration of the PromptExplorer's capabilities."""
    explorer = PromptExplorer()
    console = Console()

    # 1. Demo prompt listing
    console.print("\n[bold cyan]1. Demonstrating Prompt Listing[/bold cyan]")
    console.print("Fetching available prompts from Vellum...\n")
    prompts = explorer.list_prompts()
    explorer.display_prompts(prompts)

    if not prompts:
        console.print("[red]No prompts found. Please check your API key and permissions.[/red]")
        return

    # 2. Demo prompt execution
    console.print("\n[bold cyan]2. Demonstrating Prompt Execution[/bold cyan]")
    test_prompt = prompts[0]  # Use first available prompt
    console.print(f"Executing prompt: [green]{test_prompt.name}[/green]")
    
    # Demo inputs - using auto-seeding prompt format
    demo_inputs = {
        "description": "A friendly chatbot that helps users learn Python",
        "classification": "educational assistant",
        "context": "Python programming tutorial context",
        "domain": "education",
        "selectedLevel": "beginner",
        "instruction": "Create a helpful Python learning assistant",
        "constraints": "Keep explanations simple and beginner-friendly, use examples"  # Added final required variable
    }
    console.print("Input variables:", demo_inputs)
    
    result = explorer.execute_prompt(
        prompt_name=test_prompt.name,
        inputs=demo_inputs
    )

    if result:
        console.print("\n[green]Execution successful![/green]")
        console.print("Result:", result)
    else:
        console.print("\n[yellow]Note: This is a demo run. For actual use:[/yellow]")
        console.print("1. Use the CLI interface: [bold]vellum-explorer <command>[/bold]")
        console.print("2. Available commands: [bold]list[/bold], [bold]execute[/bold], [bold]show[/bold]")
        console.print("3. For help: [bold]vellum-explorer --help[/bold]")
        console.print("\nTip: Check the prompt's required input variables using: [bold]vellum-explorer show <prompt-name>[/bold]")


if __name__ == "__main__":
    demo_functionality()
