"""
Vellum Prompt CLI - CLI helper for LLMS to explore and execute Vellum prompts, and diagnose issues.

This module provides functionality to:
1. List available prompts - [via deployments.list endpoint, use: vellum-explorer list --status ACTIVE] - [90% complete, TODO: Add filtering by environment]
2. View prompt details - [via deployments.get endpoint, use: vellum-explorer show <prompt-name>] - [80% complete, TODO: Add version history, usage stats]
3. Execute prompts with custom inputs - [via execute_prompt endpoint, use: vellum-explorer execute <prompt-name> --inputs '{"key": "value"}'] - [95% complete, TODO: Add streaming support]
4. Save and manage prompt results - [Export to CSV/XLSX/JSON] - [100% complete]
5. Help / Code Diagnostic based on learnings - TODO: Integrate with learnings documentation for automated troubleshooting

Run this file directly to see a demo of all functionality, including CLI command examples.

v7 - Improved help display and demo
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

# Initialize Rich console with forced color output
console = Console(force_terminal=True, color_system="truecolor")

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
        v3 - Added error handling
        """
        # Initialize console first for error handling
        self.console = Console()
        self._cache = {}

        try:
            # Load environment variables if no API key provided
            if not api_key:
                api_key = os.environ.get('VELLUM_API_KEY')

            if not api_key:
                self.console.print("[red]No API key found. Please set VELLUM_API_KEY in Replit Secrets.[/red]")
                self.console.print("To add your API key:")
                self.console.print("1. Click Tools > Secrets")
                self.console.print("2. Add VELLUM_API_KEY with your API key")
                raise ValueError("Missing VELLUM_API_KEY")

            # Initialize Vellum client
            self.client = Vellum(api_key=api_key)
        except Exception as e:
            self.client = None
            if not isinstance(e, ValueError):
                self.handle_error(str(e), "environment")
                raise

    def get_help(self, topic: Optional[str] = None, error: Optional[str] = None) -> None:
        """
        Get help and guidance based on topic or error.

        1. Show all available help by default
        2. Show error-specific guidance if error provided
        3. Show topic-specific guidance if topic provided
        v2 - Now shows all help by default
        """
        if error:
            guidance = get_learning_by_error(error)
            if guidance:
                self.console.print("\n[bold cyan]Error Guidance:[/bold cyan]")
                self.console.print(guidance)

        # Show all help topics by default
        self.console.print("\n[bold cyan]CLI Usage Guide[/bold cyan]")
        self.console.print("\n[yellow]Basic Commands:[/yellow]")
        self.console.print("1. List prompts:")
        self.console.print("   vellum-explorer list")
        self.console.print("   vellum-explorer list --status ACTIVE --environment DEVELOPMENT")
        self.console.print("   vellum-explorer list --export prompts.csv")

        self.console.print("\n2. Execute prompts:")
        self.console.print("   vellum-explorer execute my-prompt --inputs '{\"key\": \"value\"}'")
        self.console.print("   vellum-explorer execute my-prompt --inputs '{\"key\": \"value\"}' --stream")
        self.console.print("   vellum-explorer execute my-prompt --inputs '{\"key\": \"value\"}' --export results.xlsx")

        self.console.print("\n3. Show prompt details:")
        self.console.print("   vellum-explorer show my-prompt")

        self.console.print("\n[yellow]Feature-specific Help:[/yellow]")
        self.console.print("\n1. Streaming Output:")
        self.console.print(get_learning_by_topic("streaming"))

        self.console.print("\n2. Export Functionality:")
        self.console.print(get_learning_by_topic("export"))

        self.console.print("\n3. Environment Management:")
        self.console.print(get_learning_by_topic("environment"))

        self.console.print("\n4. Input Handling:")
        self.console.print(get_learning_by_topic("input"))

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
        v3 - Updated to handle VellumVariable objects
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
            except BaseException:
                pass  # Version history is optional

            # Extract input variable names from VellumVariable objects
            input_variables = []
            if hasattr(deployment, 'input_variables'):
                for var in deployment.input_variables:
                    if hasattr(var, 'name'):
                        input_variables.append(var.name)
                    else:
                        input_variables.append(str(var))

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
                "input_variables": input_variables,
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
                types.PromptRequestInput(
                    name=name,
                    value=value
                )
                for name, value in inputs.items()
            ]

            # Debug log the inputs
            self.console.print("[cyan]Debug: Sending inputs to Vellum:[/cyan]")
            self.console.print(json.dumps({"inputs": [{"name": i.name, "value": i.value} for i in vellum_inputs]}, indent=2))

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
                error_detail = e.response.json()
                self.console.print(f"[red]Error response from Vellum:[/red]")
                self.console.print(json.dumps(error_detail, indent=2))
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


# -------------------- 5. MAIN EXECUTION ----------------------------------
def demo_functionality():
    """
    Run a demonstration of the PromptExplorer's capabilities.
    
    1. Show CLI usage guide
    2. List available prompts
    3. Execute example prompt
    4. Show export capabilities
    v8 - Added prominent help display
    """
    explorer = PromptExplorer()
    console = Console()

    # Show CLI usage guide first
    console.print("\n[bold cyan]Vellum Prompt Explorer - Quick Start Guide[/bold cyan]")
    console.print("\n[yellow]Available Commands:[/yellow]")
    console.print("1. List prompts:")
    console.print("   vellum-explorer list")
    console.print("   vellum-explorer list --status ACTIVE --environment DEVELOPMENT")
    console.print("   vellum-explorer list --export prompts.csv")
    
    console.print("\n2. Execute prompts:")
    console.print("   vellum-explorer execute my-prompt --inputs '{\"key\": \"value\"}'")
    console.print("   vellum-explorer execute my-prompt --inputs '{\"key\": \"value\"}' --export results.xlsx")
    
    console.print("\n3. Environment setup:")
    console.print("   - Create .env file with VELLUM_API_KEY=your-api-key")
    console.print("   - Or set environment variable: export VELLUM_API_KEY=your-api-key")
    
    console.print("\n4. Export formats:")
    console.print("   - CSV:  --export results.csv")
    console.print("   - XLSX: --export results.xlsx")
    console.print("   - JSON: --export results.json")

    console.print("\n[bold cyan]Starting Demo...[/bold cyan]")
    console.print("This demo shows the main features of the CLI tool.\n")

    # Rest of the demo
    # 1. Show help information
    console.print("\n[bold cyan]1. Help Information[/bold cyan]")
    console.print("Detailed help and guidance:")
    explorer.get_help()

    # 2. Demo prompt listing
    console.print("\n[bold cyan]2. Prompt Listing Demo[/bold cyan]")
    console.print("Now, let's list available prompts from Vellum:")
    prompts = explorer.list_prompts()
    explorer.display_prompts(prompts)

    if not prompts:
        console.print("[red]No prompts found. Please check your API key and permissions.[/red]")
        return

    # 3. Demo prompt execution
    console.print("\n[bold cyan]3. Prompt Execution Demo[/bold cyan]")
    test_prompt = prompts[0]
    console.print(f"Let's execute the first available prompt: [green]{test_prompt.name}[/green]")

    # Demo inputs
    demo_inputs = {
        "description": "A friendly chatbot that helps users learn Python",
        "classification": "educational assistant",
        "context": "Python programming tutorial context",
        "domain": "education",
        "selectedLevel": "beginner",
        "instruction": "Create a helpful Python learning assistant",
        "constraints": "Keep explanations simple and beginner-friendly, use examples"
    }
    console.print("\nUsing these example inputs:")
    console.print(demo_inputs)

    console.print("\nExecuting prompt...")
    result = explorer.execute_prompt(
        prompt_name=test_prompt.name,
        inputs=demo_inputs
    )

    if result:
        console.print("\n[green]Execution successful![/green]")
        console.print("Result:", result)

    # 4. Show export capabilities
    console.print("\n[bold cyan]4. Export Capabilities[/bold cyan]")
    console.print("The CLI supports exporting results to CSV, XLSX, and JSON formats.")
    console.print("Example commands:")
    console.print("1. Export prompt list:   vellum-explorer list --export prompts.csv")
    console.print("2. Export execution:     vellum-explorer execute my-prompt --inputs '{...}' --export results.xlsx")

    console.print("\n[bold cyan]Try It Yourself[/bold cyan]")
    console.print("1. Set your VELLUM_API_KEY in .env")
    console.print("2. Run 'vellum-explorer --help' to see all commands")
    console.print("3. Use the example commands shown above")


if __name__ == "__main__":
    demo_functionality()
