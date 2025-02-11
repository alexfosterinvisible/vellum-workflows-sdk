import streamlit as st
import subprocess
import os
from pathlib import Path

# Configure Streamlit page
st.set_page_config(
    page_title="Vellum Prompt Explorer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for terminal-like appearance matching Rich output
st.markdown("""
<style>
    /* Main background and text */
    .stApp {
        background-color: #1a1b26;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #1a1b26;
        color: #a9b1d6;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #1a1b26 !important;
        color: #a9b1d6 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Code blocks and pre formatting */
    pre {
        background-color: #1a1b26 !important;
        padding: 10px !important;
        border-radius: 5px !important;
        margin: 10px 0 !important;
    }
    
    /* Rich text colors */
    .user-cmd {
        color: #7aa2f7 !important;
    }
    .prompt-name {
        color: #9ece6a !important;
    }
    .status-active {
        color: #9ece6a !important;
    }
    .environment {
        color: #7dcfff !important;
    }
    .timestamp {
        color: #a9b1d6 !important;
    }
    .section-header {
        color: #bb9af7 !important;
        font-weight: bold !important;
    }
    
    /* Table styling */
    table {
        color: #a9b1d6 !important;
        background-color: #1a1b26 !important;
    }
    th {
        background-color: #1a1b26 !important;
        color: #7aa2f7 !important;
        border-color: #565f89 !important;
    }
    td {
        background-color: #1a1b26 !important;
        border-color: #565f89 !important;
    }
    
    /* Spinner styling */
    .stSpinner > div > div > div {
        border-left-color: #7aa2f7 !important;
        border-right-color: #7aa2f7 !important;
        border-bottom-color: #7aa2f7 !important;
    }
    
    /* Chat input container */
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
        color: #a9b1d6 !important;
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

def format_output(text: str) -> str:
    """Format the output with Rich-like styling using HTML."""
    # Add custom styling for different elements
    text = text.replace("Available Commands:", "<span class='section-header'>Available Commands:</span>")
    text = text.replace("Basic Commands:", "<span class='section-header'>Basic Commands:</span>")
    text = text.replace("Feature-specific Help:", "<span class='section-header'>Feature-specific Help:</span>")
    text = text.replace("ACTIVE", "<span class='status-active'>ACTIVE</span>")
    text = text.replace("DEVELOPMENT", "<span class='environment'>DEVELOPMENT</span>")
    return text

def run_command(cmd: str, show_command: bool = True) -> None:
    """Execute a command and display its output with loading indicator."""
    if show_command:
        st.chat_message("user").markdown(f"<span class='user-cmd'>$ {cmd}</span>", unsafe_allow_html=True)
        st.session_state.history.append(cmd)
    
    with st.spinner('Executing command...'):
        try:
            result = subprocess.run(
                ["python", str(current_dir / "prompt_explorer.py")] + cmd.split(),
                capture_output=True,
                text=True,
                env=os.environ.copy()
            )
            
            # Display the output
            if result.stdout:
                formatted_output = format_output(result.stdout)
                st.chat_message("assistant").markdown(f"```\n{formatted_output}\n```", unsafe_allow_html=True)
            
            # Show errors if any
            if result.stderr:
                st.chat_message("assistant").markdown(
                    f"<span style='color: #f7768e'>**Error Output**: \n```\n{result.stderr}\n```</span>",
                    unsafe_allow_html=True
                )
                
        except Exception as e:
            st.chat_message("assistant").markdown(
                f"<span style='color: #f7768e'>**Error**: \n```\n{str(e)}\n```</span>",
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
            st.markdown(f"<span class='user-cmd'>$ {cmd}</span>", unsafe_allow_html=True)
