import streamlit as st
import subprocess
import os
from pathlib import Path
from ansi2html import Ansi2HTMLConverter

# Configure Streamlit page
st.set_page_config(
    page_title="Vellum Prompt Explorer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for terminal-like appearance
st.markdown("""
<style>
    .stApp {
        background-color: #1a1b26;
    }
    
    .stChatMessage {
        background-color: #1a1b26 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    .stChatInputContainer {
        background-color: #1a1b26 !important;
        border-color: #565f89 !important;
    }
    
    /* Command history */
    .streamlit-expanderHeader {
        background-color: #1a1b26 !important;
        color: #7aa2f7 !important;
    }
    .streamlit-expanderContent {
        background-color: #1a1b26 !important;
    }
    
    /* Spinner styling */
    .stSpinner > div > div > div {
        border-left-color: #7aa2f7 !important;
        border-right-color: #7aa2f7 !important;
        border-bottom-color: #7aa2f7 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for command history and first run
if 'history' not in st.session_state:
    st.session_state.history = []
if 'first_run' not in st.session_state:
    st.session_state.first_run = True

# Get the directory of the current script
current_dir = Path(__file__).parent

# Initialize ANSI to HTML converter
conv = Ansi2HTMLConverter()

def run_command(cmd: str, show_command: bool = True) -> None:
    """Execute a command and display its output with loading indicator."""
    if show_command:
        st.chat_message("user").markdown(f"```$ {cmd}```")
        st.session_state.history.append(cmd)
    
    with st.spinner('Executing command...'):
        try:
            # Set environment variables to force color output
            env = os.environ.copy()
            env['FORCE_COLOR'] = '1'
            env['PYTHONIOENCODING'] = 'utf-8'
            
            result = subprocess.run(
                ["python", str(current_dir / "prompt_explorer.py")] + cmd.split(),
                capture_output=True,
                text=True,
                env=env
            )
            
            # Display the output with preserved colors
            if result.stdout:
                html_output = conv.convert(result.stdout, full=False)
                st.chat_message("assistant").markdown(html_output, unsafe_allow_html=True)
            
            # Show errors if any
            if result.stderr:
                html_err = conv.convert(result.stderr, full=False)
                st.chat_message("assistant").markdown(
                    f"**[Error Output]:**<br>{html_err}",
                    unsafe_allow_html=True
                )
                
        except Exception as e:
            st.chat_message("assistant").markdown(
                f"**Error**: ```\n{str(e)}\n```",
                unsafe_allow_html=True
            )

# Run demo on first load
if st.session_state.first_run:
    run_command("", show_command=False)
    st.session_state.first_run = False

# Provide a single chat input like a terminal prompt
command = st.chat_input("vellum-explorer > ")

if command:
    run_command(command)

# Show command history at the bottom
if st.session_state.history:
    with st.expander("Command History", expanded=False):
        for cmd in reversed(st.session_state.history):
            st.markdown(f"```$ {cmd}```")
