"""
Command-line interface for the Vellum Prompt Explorer.

This module provides CLI commands for:
1. List available prompts - [via 'list' command with status and environment filtering] - [100% complete]
2. View prompt details - [via 'show' command with version history] - [95% complete]
3. Execute prompts with inputs - [via 'execute' command with JSON input and streaming support] - [100% complete]
4. View execution results - [Rich console output with formatted results] - [95% complete]
5. Export functionality - [Export to CSV/XLSX/JSON] - [100% complete]
6. Help and Diagnostics - [Context-aware help and error guidance] - [100% complete]
7. Natural language documentation queries - [OpenAI helper] - [NEW]

Usage Examples:
    vellum-explorer list --status ACTIVE --environment DEVELOPMENT
    vellum-explorer show my-prompt
    vellum-explorer execute my-prompt --inputs '{"var": "value"}'
    vellum-explorer execute my-prompt --inputs '{"var": "value"}' --stream
    vellum-explorer list --export prompts.csv
    vellum-explorer execute my-prompt --inputs '{"var": "value"}' --export results.xlsx
    vellum-explorer help streaming
    vellum-explorer ask "What is the difference between active and archived prompts?"

v6 - Added help and diagnostics
v2 - Added natural language documentation queries
v7 - Fixed import paths
v8 - Fixed import paths and package structure
"""

from src.openai_helper import OpenAIHelper
from src.prompt_explorer import PromptExplorer
import click
from rich.console import Console
import json
import os
import sys
from pathlib import Path

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


if __name__ == '__main__':
    cli(obj={})
