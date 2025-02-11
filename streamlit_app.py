import streamlit as st
import io
import json
from rich.console import Console

# Import PromptExplorer from the existing CLI module
# Adjust the import path if necessary
from prompts_CLI.src.prompt_explorer import PromptExplorer


def get_rich_console() -> (Console, io.StringIO):
    """Return a Rich Console that writes to a StringIO buffer."""
    buffer = io.StringIO()
    console = Console(file=buffer, force_terminal=True, color_system="truecolor")
    return console, buffer

# Initialize session state for terminal history and the PromptExplorer instance
if 'terminal_history' not in st.session_state:
    st.session_state.terminal_history = ""
if 'explorer' not in st.session_state:
    st.session_state.explorer = PromptExplorer()


def process_command(command: str) -> str:
    """Process the command input and return the captured Rich console output."""
    explorer: PromptExplorer = st.session_state.explorer
    rich_console, buffer = get_rich_console()
    # Temporarily override the explorer's console with our Rich console
    old_console = explorer.console
    explorer.console = rich_console
    
    try:
        parts = command.strip().split()
        if not parts:
            rich_console.print("[yellow]No command entered.[/yellow]")
        else:
            cmd = parts[0].lower()
            if cmd == "help":
                explorer.get_help()
            elif cmd == "list":
                prompts = explorer.list_prompts()
                explorer.display_prompts(prompts)
            elif cmd == "show":
                if len(parts) < 2:
                    rich_console.print("[red]Usage: show <prompt_name>[/red]")
                else:
                    prompt_name = parts[1]
                    details = explorer.get_prompt_details(prompt_name)
                    if details:
                        explorer.display_prompt_details(details)
                    else:
                        rich_console.print(f"[red]Prompt '{prompt_name}' not found.[/red]")
            elif cmd == "execute":
                if len(parts) < 2:
                    rich_console.print("[red]Usage: execute <prompt_name> --inputs '{\"key\": \"value\"}'[/red]")
                else:
                    prompt_name = parts[1]
                    try:
                        inputs_flag_index = parts.index("--inputs")
                        inputs_str = " ".join(parts[inputs_flag_index + 1:])
                        try:
                            inputs_dict = json.loads(inputs_str)
                        except Exception as e:
                            rich_console.print(f"[red]Invalid JSON for inputs: {e}[/red]")
                            inputs_dict = {}
                    except ValueError:
                        rich_console.print("[red]No inputs provided. Usage: execute <prompt_name> --inputs '{\"key\": \"value\"}'[/red]")
                        inputs_dict = {}
                    result = explorer.execute_prompt(prompt_name, inputs_dict)
                    if result:
                        rich_console.print("[green]Execution successful![/green]")
                        rich_console.print("Result:", result)
                    else:
                        rich_console.print("[red]Execution failed or returned no result.[/red]")
            elif cmd == "clear":
                st.session_state.terminal_history = ""
                rich_console.print("[cyan]Terminal cleared.[/cyan]")
            else:
                rich_console.print(f"[red]Unknown command: {cmd}[/red]")
    except Exception as e:
        rich_console.print(f"[red]Error processing command: {e}[/red]")
    finally:
        explorer.console = old_console
    
    output = buffer.getvalue()
    return output


st.title("Vellum Prompt Explorer - Terminal Emulator")

# Display terminal history in a disabled text area (simulating a terminal output)
terminal_area = st.text_area("Terminal", value=st.session_state.terminal_history, height=400, disabled=True)

# Input field for commands
command = st.text_input("Enter command", key="command_input")

if st.button("Submit Command"):
    if command:
        output = process_command(command)
        st.session_state.terminal_history += f"> {command}\n{output}\n"
        # Clear the input
        st.session_state.command_input = ""
        st.experimental_rerun() 