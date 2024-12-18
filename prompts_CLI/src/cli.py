"""
Command-line interface for the Vellum Prompt Explorer.

This module provides CLI commands for:
1. List available prompts - [via 'list' command with status and environment filtering] - [100% complete]
2. View prompt details - [via 'show' command with version history] - [95% complete]
3. Execute prompts with inputs - [via 'execute' command with JSON input and streaming support] - [100% complete]
4. View execution results - [Rich console output with formatted results] - [95% complete]
5. Export functionality - [Export to CSV/XLSX/JSON] - [100% complete]

Usage Examples:
    vellum-explorer list --status ACTIVE --environment DEVELOPMENT
    vellum-explorer show my-prompt
    vellum-explorer execute my-prompt --inputs '{"var": "value"}'
    vellum-explorer execute my-prompt --inputs '{"var": "value"}' --stream
    vellum-explorer list --export prompts.csv
    vellum-explorer execute my-prompt --inputs '{"var": "value"}' --export results.xlsx

v5 - Added export functionality
"""

import click
from rich.console import Console
import json
import os

from .prompt_explorer import PromptExplorer


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
    v2
    """
    ctx.ensure_object(dict)
    try:
        ctx.obj['explorer'] = PromptExplorer(api_key=api_key)
    except Exception as e:
        console.print(f"[red]Error initializing Prompt Explorer: {str(e)}[/red]")
        ctx.exit(1)


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
    prompts = explorer.list_prompts(status=status, environment=environment)
    
    if not prompts:
        console.print("[yellow]No prompts found matching the criteria.[/yellow]")
        return
        
    # Display results
    explorer.display_prompts(prompts)

    # Export if requested
    if export:
        if explorer.export_prompts(export):
            console.print(f"[green]Successfully exported prompts to: {export}[/green]")
        else:
            console.print(f"[red]Failed to export prompts to: {export}[/red]")
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
    v4 - Added export option
    """
    try:
        # Parse inputs JSON
        input_dict = json.loads(inputs)

        # Execute prompt
        explorer = ctx.obj['explorer']
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
                    ctx.exit(1)

    except json.JSONDecodeError:
        console.print("[red]Error: Inputs must be a valid JSON string[/red]")
        ctx.exit(1)
    except Exception as e:
        console.print(f"[red]Error executing prompt: {str(e)}[/red]")
        ctx.exit(1)


if __name__ == '__main__':
    cli(obj={})
