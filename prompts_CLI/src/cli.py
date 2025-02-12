"""
Command-line interface for the Vellum Prompt Explorer.

This module provides CLI commands for:
1. List available prompts - [via 'list' command with status and environment filtering] - [100% complete]
2. View prompt details - [via 'inspect' command with version history] - [95% complete]
3. Execute prompts with inputs - [via 'execute' command with JSON input and streaming support] - [100% complete]
4. View execution results - [Rich console output with formatted results] - [95% complete]
5. Export functionality - [Export to CSV/XLSX/JSON] - [100% complete]
6. Help and Diagnostics - [Context-aware help and error guidance] - [100% complete]
7. Natural language documentation queries - [OpenAI helper] - [100% complete]
8. Combined list and inspect - [via 'list-and-inspect' command] - [NEW]
   - After returning the table, it then calls inspect in parallel for each prompt returned in the list
   - Prints a complete JSON then a more advanced rich table with core information
   - Includes variable names and all information required to run the prompt
   - Never concatenates the variables list to maintain all values

Usage Examples:
    vellum-explorer list --status ACTIVE --environment DEVELOPMENT
    vellum-explorer show my-prompt
    vellum-explorer list-and-inspect
    vellum-explorer list-and-inspect --status ACTIVE
    vellum-explorer ask "What is the difference between active and archived prompts?"
    vellum-explorer execute my-prompt --inputs '{"var": "value"}'
    vellum-explorer execute my-prompt --inputs '{"var": "value"}' --stream
    vellum-explorer list --export prompts.csv
    vellum-explorer execute my-prompt --inputs '{"var": "value"}' --export results.xlsx
    vellum-explorer help streaming

TODO:
1. Add filtering to list command:
   - Filter by model type
   - Filter by last used date
   - Filter by input variable types
   - Filter by usage frequency
2. Add sorting options to list command
3. Add pagination for large lists
4. Add search by regex pattern
5. Add comparison view between prompts

v10 - Renamed overview to list-and-inspect for clarity
"""

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .openai_helper import OpenAIHelper
from .prompt_explorer import PromptExplorer

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))


console = Console()


@click.group()
@click.option('--api-key', envvar='VELLUM_API_KEY', help='Vellum API key')
@click.pass_context
def cli(ctx, api_key):
    """
    Vellum Prompt Explorer CLI - Main entry point.

    1. Initialize explorer with API key
    2. Set up context for subcommands
    3. Handle initialization errors
    v3 - Added quick guide display
    """
    ctx.ensure_object(dict)
    console = Console()

    # Always show quick guide first
    console.print("\n[bold cyan]Vellum Prompt Explorer - Quick Start Guide[/bold cyan]")
    console.print("\n[yellow]Available Commands:[/yellow]")
    console.print("1. List prompts:")
    console.print("   vellum-explorer list")
    console.print("   vellum-explorer list --status ACTIVE --environment DEVELOPMENT")
    console.print("   vellum-explorer list --export prompts.csv")

    console.print("\n2. Inspect prompt:")
    console.print("   vellum-explorer inspect <prompt-name>")
    console.print("   [Shows required inputs, versions, and deployment details]")

    console.print("\n3. Get detailed overview:")
    console.print("   vellum-explorer list-and-inspect")
    console.print("   vellum-explorer list-and-inspect --status ACTIVE --environment DEVELOPMENT")
    console.print("   [Combined list and inspect - shows all prompts with their inputs]")

    console.print("\n4. Execute prompts:")
    console.print("   vellum-explorer execute my-prompt --inputs '{\"key\": \"value\"}'")
    console.print("   vellum-explorer execute my-prompt --inputs '{\"key\": \"value\"}' --export results.xlsx")

    console.print("\n5. Ask questions:")
    console.print("   vellum-explorer ask \"How do I use environment variables?\"")
    console.print("   [Natural language help - uses AI to answer questions about Vellum]")

    console.print("\n6. Environment setup:")
    console.print("   - Create .env file with VELLUM_API_KEY=your-api-key")
    console.print("   - Or set environment variable: export VELLUM_API_KEY=your-api-key")

    console.print("\n7. Export formats:")
    console.print("   - CSV:  --export results.csv")
    console.print("   - XLSX: --export results.xlsx")
    console.print("   - JSON: --export results.json")

    console.print("\n[cyan]Executing command...[/cyan]\n")

    try:
        ctx.obj['explorer'] = PromptExplorer(api_key=api_key)
    except Exception as e:
        explorer = PromptExplorer()  # Create without API key for help
        explorer.handle_error(str(e), "environment")
        ctx.exit(1)


@cli.command()
@click.argument('topic', required=False)
@click.pass_context
def help(ctx, topic):
    """
    Get help and guidance on using the CLI.

    1. Show topic-specific help if provided
    2. Show error-specific guidance if relevant
    3. Display available topics
    v1
    """
    explorer = ctx.obj['explorer']
    explorer.get_help(topic=topic)


@cli.command()
@click.option('--status', default='ACTIVE', help='Filter by status (ACTIVE/ARCHIVED)')
@click.option('--environment', help='Filter by environment (e.g., DEVELOPMENT, PRODUCTION)')
@click.option('--export', help='Export results to file (supported formats: csv, xlsx, json)')
@click.pass_context
def list(ctx, status, environment, export):
    """
    List available prompts with optional filtering.

    1. Get prompts from explorer with filters
    2. Display formatted table
    3. Export results if requested
    v4 - Added export option
    """
    explorer = ctx.obj['explorer']
    try:
        prompts = explorer.list_prompts(status=status, environment=environment)

        if not prompts:
            console.print("[yellow]No prompts found matching the criteria.[/yellow]")
            explorer.get_help(topic="environment")
            return

        # Display results
        explorer.display_prompts(prompts)

        # Export if requested
        if export:
            if explorer.export_prompts(export):
                console.print(f"[green]Successfully exported prompts to: {export}[/green]")
            else:
                console.print(f"[red]Failed to export prompts to: {export}[/red]")
                explorer.get_help(topic="export")
                ctx.exit(1)
    except Exception as e:
        explorer.handle_error(str(e), "environment")
        ctx.exit(1)


@cli.command()
@click.argument('prompt-name')
@click.option('--inputs', required=True, help='JSON string of input variables (e.g., \'{"var1": "value1", "var2": "value2"}\')')
@click.option('--release-tag', default='LATEST', help='Release tag to use (default: LATEST)')
@click.option('--stream', is_flag=True, help='Enable streaming output (disables Rich formatting)')
@click.option('--export', help='Export results to file (supported formats: csv, xlsx, json)')
@click.pass_context
def execute(ctx, prompt_name, inputs, release_tag, stream, export):
    """
    Execute a prompt with given inputs.

    1. Parse and validate JSON inputs
    2. Execute prompt with explorer
    3. Format and display results
    4. Export results if requested
    v5 - Added learnings integration
    """
    explorer = ctx.obj['explorer']
    try:
        # Parse inputs JSON
        try:
            input_dict = json.loads(inputs)
        except json.JSONDecodeError:
            explorer.handle_error("Invalid JSON input format", "input")
            ctx.exit(1)

        # Execute prompt
        result = explorer.execute_prompt(
            prompt_name=prompt_name,
            inputs=input_dict,
            release_tag=release_tag,
            stream=stream
        )

        # Display results for non-streaming execution
        if result and not stream:
            console.print("\n[green]Prompt Execution Result:[/green]")

            # Convert Vellum values to plain Python types
            output_list = []
            for item in result:
                if hasattr(item, 'value'):
                    output_list.append(item.value)
                else:
                    output_list.append(str(item))

            # Format and display the output
            for i, output in enumerate(output_list, 1):
                console.print(f"\n[yellow]Output {i}:[/yellow]")
                console.print(output)

            # Export if requested
            if export and not stream:
                if explorer.export_execution_result(result, export):
                    console.print(f"[green]Successfully exported results to: {export}[/green]")
                else:
                    console.print(f"[red]Failed to export results to: {export}[/red]")
                    explorer.get_help(topic="export")
                    ctx.exit(1)

    except Exception as e:
        explorer.handle_error(str(e), "input")
        ctx.exit(1)


@cli.command()
@click.argument('question', type=str)
def ask(question: str):
    """
    Ask a natural language question about Vellum documentation.

    1. Initialize OpenAI helper
    2. Query documentation in parallel
    3. Display formatted results
    v1 - Initial implementation
    """
    try:
        # Initialize helper
        helper = OpenAIHelper(use_md_crawler=True)

        # Query documentation
        console.print(f"\n[cyan]Searching documentation for:[/cyan] {question}\n")
        result = helper.query_docs_parallel(question)

        # Display answer
        console.print("[bold green]Answer:[/bold green]")
        console.print(result.get("answer", "No answer available"))

        # Display supporting evidence
        if quotes := result.get("quotes", []):
            console.print("\n[bold yellow]Supporting Evidence:[/bold yellow]")
            for quote in quotes:
                if quote.get("is_code", False):
                    console.print(f"\n[magenta]Code Example:[/magenta] (from {quote.get('source', 'unknown')})")
                    console.print(quote.get("text", ""))
                else:
                    console.print(f"\n[yellow]Quote:[/yellow] (from {quote.get('source', 'unknown')})")
                    console.print(quote.get("text", ""))
                console.print(f"[dim]Relevance:[/dim] {quote.get('relevance', '')}")

        # Display confidence scores
        if confidence := result.get("confidence", {}):
            console.print("\n[bold blue]Confidence Scores:[/bold blue]")
            console.print(f"Answer Quality: {confidence.get('answer_quality', 'N/A')}")
            console.print(f"Source Quality: {confidence.get('source_quality', 'N/A')}")
            console.print(f"Completeness: {confidence.get('completeness', 'N/A')}")
            console.print(f"Code Examples: {confidence.get('code_examples', 'N/A')}")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.argument('prompt-name')
@click.pass_context
def inspect(ctx, prompt_name):
    """
    Inspect detailed information about a specific prompt.

    1. Get prompt details and configuration
    2. Display required input variables
    3. Show version history and deployment status
    4. Display model and environment info
    v1 - Initial implementation
    """
    explorer = ctx.obj['explorer']
    try:
        # Get prompt details
        details = explorer.get_prompt_details(prompt_name)
        if not details:
            console.print(f"[red]No prompt found with name: {prompt_name}[/red]")
            return

        # Display details
        explorer.display_prompt_details(details)

    except Exception as e:
        explorer.handle_error(str(e), "prompt")
        ctx.exit(1)


@cli.command()
@click.option('--status', default='ACTIVE', help='Filter by status (ACTIVE/ARCHIVED)')
@click.option('--environment', help='Filter by environment (e.g., DEVELOPMENT, PRODUCTION)')
@click.option('--export', help='Export results to file (supported formats: csv, xlsx, json)')
@click.pass_context
def list_and_inspect(ctx, status, environment, export):
    """
    Combined list and inspect command - shows detailed overview of all prompts.

    1. List all prompts in table format
    2. Get detailed info for each prompt in parallel
    3. Display comprehensive overview with input variables
    4. Export combined data if requested
    v3 - Renamed from overview for clarity
    """
    explorer = ctx.obj['explorer']
    console = Console()

    try:
        # Get list of prompts
        prompts = explorer.list_prompts(status=status, environment=environment)
        if not prompts:
            console.print("[yellow]No prompts found matching the criteria.[/yellow]")
            explorer.get_help(topic="environment")
            return

        # Display initial table
        console.print("\n[bold cyan]Available Prompts - Basic Overview[/bold cyan]")
        explorer.display_prompts(prompts)

        # Get details for each prompt
        console.print("\n[bold cyan]Fetching detailed information for all prompts...[/bold cyan]")
        details = []
        for prompt in prompts:
            try:
                detail = explorer.get_prompt_details(prompt.name)
                if detail:
                    details.append(detail)
            except Exception as e:
                console.print(f"[yellow]Warning: Could not fetch details for {prompt.name}: {str(e)}[/yellow]")

        if not details:
            console.print("[red]Could not fetch details for any prompts.[/red]")
            return

        # Display JSON/Dict view
        console.print("\n[bold cyan]Detailed Overview (JSON/Dict format)[/bold cyan]")
        for detail in details:
            console.print(f"\n[magenta]{detail['name']}[/magenta]")

            # Extract variable info safely
            input_vars = []
            for var in detail.get('input_variables', []):
                try:
                    if isinstance(var, dict):
                        var_info = {
                            'key': var.get('key', 'Unknown'),
                            'type': var.get('type', 'Unknown'),
                            'required': var.get('required', None)
                        }
                    else:
                        var_info = {
                            'key': var.split("key='")[1].split("'")[0] if "key='" in var else 'Unknown',
                            'type': var.split("type='")[1].split("'")[0] if "type='" in var else 'Unknown',
                            'required': var.split("required=")[1].split(" ")[0] if "required=" in var else None
                        }
                    input_vars.append(var_info)
                except Exception:
                    continue

            # Create overview dict
            overview = {
                'environment': detail['environment'],
                'status': detail['status'],
                'model': detail.get('model', 'Unknown'),
                'last_used': detail['last_deployed'].strftime("%Y-%m-%d %H:%M:%S"),
                'input_variables': input_vars
            }

            console.print(overview)

        # Create enhanced table with input variables
        console.print("\n[bold cyan]Detailed Prompt Overview[/bold cyan]")
        table = Table(
            title="Prompt Details",
            show_header=True,
            header_style="bold magenta",
            show_lines=True,  # Add lines between rows for better readability
            pad_edge=True,    # Add padding at table edges
            expand=True       # Allow table to use full width
        )
        table.add_column("Prompt Info", style="cyan", width=40, no_wrap=True)
        table.add_column("Input Variables", style="magenta", min_width=80)  # Allow wrapping but ensure minimum width

        for detail in details:
            # Format prompt info
            prompt_info = (
                f"[bold]{detail['name']}[/bold]\n"
                f"[dim]Environment:[/dim] {detail['environment']}\n"
                f"[dim]Status:[/dim] {detail['status']}\n"
                f"[dim]Model:[/dim] {detail.get('model', 'Unknown')}\n"
                f"[dim]Last Used:[/dim] {detail['last_deployed'].strftime('%Y-%m-%d %H:%M:%S')}"
            )

            # Format input variables more cleanly
            input_vars = []
            for var_info in detail.get('input_variables', []):
                try:
                    if isinstance(var_info, dict):
                        key = var_info.get('key', 'Unknown')
                        type_ = var_info.get('type', 'Unknown')
                        required = var_info.get('required', None)
                    else:
                        # Parse the string representation
                        key = var_info.split("key='")[1].split("'")[0] if "key='" in var_info else var_info
                        type_ = var_info.split("type='")[1].split("'")[0] if "type='" in var_info else "Unknown"
                        required = var_info.split("required=")[1].split(" ")[0] if "required=" in var_info else None

                    input_vars.append(f"• {key} [dim](type={type_}, required={required})[/dim]")
                except Exception:
                    continue

            input_vars_str = "\n".join(sorted(input_vars)) if input_vars else "No inputs required"

            table.add_row(prompt_info, input_vars_str)

        console.print(table)

        # Export if requested
        if export:
            # Convert to exportable format
            export_data = [{
                'name': d['name'],
                'environment': d['environment'],
                'status': d['status'],
                'model': d.get('model', 'Unknown'),
                'input_variables': d.get('input_variables', []),
                'last_used': d['last_deployed'].strftime("%Y-%m-%d %H:%M:%S"),
                'description': d.get('description', ''),
                'versions': d.get('versions', [])
            } for d in details]

            if explorer.export_prompts(export_data, export):  # Pass export_data to export_prompts
                console.print(f"[green]Successfully exported detailed overview to: {export}[/green]")
            else:
                console.print(f"[red]Failed to export overview to: {export}[/red]")
                explorer.get_help(topic="export")
                ctx.exit(1)

    except Exception as e:
        console.print(f"[red]Error in list-and-inspect command: {str(e)}[/red]")
        ctx.exit(1)


if __name__ == '__main__':
    cli(obj={})
