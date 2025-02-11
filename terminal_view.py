import streamlit as st
from ansi2html import Ansi2HTMLConverter


class CONFIG:
    """General configuration options for the terminal view."""
    LINE_HEIGHT: int = 20



def display_terminal_output_colored(terminal_output: str) -> None:
    """
    Display terminal output line by line with colored formatting in Streamlit.

    This function splits the terminal output into individual lines, converts ANSI color codes into HTML,
    and displays each line along with its line number using st.markdown.

    Args:
        terminal_output (str): The terminal output containing ANSI color codes.
    """
    conv = Ansi2HTMLConverter(inline=True)
    for idx, line in enumerate(terminal_output.splitlines(), start=1):
        html_line = conv.convert(line, full=False)
        # Each line is rendered with its line number and converted HTML from ANSI codes
        st.markdown(f"<div style='white-space: pre-wrap; font-family: monospace; margin:0;'>Line {idx}: {html_line}</div>", unsafe_allow_html=True)



def main() -> None:
    """
    Main function to launch the terminal output viewer in Streamlit.

    It provides a text area for inputting terminal output and processes it line by line with colored formatting.
    """
    st.title("Terminal Output Viewer (Line-by-Line with Colors)")
    default_text = ("\x1b[31mError:\x1b[0m Something went wrong...\n"
                    "\x1b[32mSuccess:\x1b[0m Operation completed successfully.\n"
                    "\x1b[33mWarning:\x1b[0m Check your configuration settings.")
    terminal_output = st.text_area("Paste your terminal output below:", value=default_text, height=150)

    st.sidebar.subheader("Raw Terminal Output")
    st.sidebar.text(terminal_output)

    st.header("Formatted Terminal Output")
    display_terminal_output_colored(terminal_output)


if __name__ == "__main__":
    main() 