import streamlit as st
import json
import pandas as pd
import os
import sys
from pathlib import Path

# Add the project root to Python path for both local and Replit environments
try:
    # Local development - go up two levels from this file
    project_root = str(Path(__file__).parent.parent.parent)
    if project_root not in sys.path:
        sys.path.append(project_root)
    from prompts_CLI.src.prompt_explorer import PromptExplorer
except ImportError:
    try:
        # Replit environment - try direct import
        from prompt_explorer import PromptExplorer
    except ImportError:
        st.error("❌ Could not import PromptExplorer. Please check your Python path.")
        st.stop()

# Set page config for expanded width and full height
st.set_page_config(
    page_title="Vellum Prompt Explorer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for better spacing and styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        padding: 10px 20px;
        margin-bottom: 10px;
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(224, 240, 255, 0.2);
        border-color: #E0F0FF;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    .main > div {
        padding-top: 2rem;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize PromptExplorer instance
if 'explorer' not in st.session_state:
    vellum_api_key = None
    
    # Try to get API key from Streamlit secrets (primary source for Streamlit Cloud)
    try:
        if hasattr(st.secrets, "VELLUM_API_KEY"):
            vellum_api_key = st.secrets.VELLUM_API_KEY
            st.success("✅ Successfully loaded API key from Streamlit secrets")
    except Exception as e:
        st.warning(f"⚠️ Could not load from Streamlit secrets: {str(e)}")
    
    # Only try environment variables if secrets failed (fallback for local development)
    if not vellum_api_key:
        try:
            from dotenv import load_dotenv
            # Suppress dotenv warnings/errors since we know it might be broken
            try:
                load_dotenv(verbose=False)
            except Exception:
                pass
            vellum_api_key = os.getenv('VELLUM_API_KEY')
            if vellum_api_key:
                st.success("✅ Successfully loaded API key from environment variables")
        except ImportError:
            pass  # Silently fail if python-dotenv isn't available
    
    if not vellum_api_key:
        st.error("""
        ❌ No Vellum API key found. For Streamlit Cloud deployment:
        1. Go to your app's dashboard on https://share.streamlit.io
        2. Navigate to ⚙️ -> Settings -> Secrets
        3. Add your secret: VELLUM_API_KEY=your_key_here
        
        For local development:
        1. Create .streamlit/secrets.toml with:
           VELLUM_API_KEY = "your_key_here"
        """)
        st.stop()
    
    try:
        st.session_state.explorer = PromptExplorer(api_key=vellum_api_key)
        st.success("✅ Successfully initialized Vellum Prompt Explorer")
    except Exception as e:
        st.error(f"❌ Failed to initialize Vellum Prompt Explorer: {str(e)}")
        st.stop()

def display_help() -> None:
    """Display help information using Streamlit components."""
    st.header("Vellum Prompt Explorer Guide")
    
    # Quick Start
    st.subheader("🚀 Quick Start")
    st.info("""
    1. Use the **List Prompts** tab to view all available prompts
    2. Click on a prompt to view its details
    3. Use the **Execute Prompt** tab to run prompts with custom inputs
    """)
    
    # Features Overview
    st.subheader("✨ Features")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 📋 Prompt Management")
        st.markdown("""
        - View all available prompts
        - Filter by environment and status
        - Export prompt lists to CSV/XLSX
        - View detailed prompt information
        """)
        
        st.markdown("##### 🔄 Environment Control")
        st.markdown("""
        - Switch between environments
        - Set API keys securely
        - Track deployment status
        """)
    
    with col2:
        st.markdown("##### ⚡ Execution Options")
        st.markdown("""
        - Execute prompts with custom inputs
        - Stream output in real-time
        - Export results in multiple formats
        - View execution history
        """)
        
        st.markdown("##### 📊 Data Export")
        st.markdown("""
        - CSV format for spreadsheets
        - XLSX for Excel compatibility
        - JSON for data processing
        """)

def display_prompts(prompts) -> None:
    """Display prompts using Streamlit's dataframe with enhanced styling."""
    if not prompts:
        st.warning("No prompts found in the current environment.")
        return
    
    # Convert prompts to DataFrame
    data = []
    for p in prompts:
        data.append({
            "Name": p.name,
            "Label": p.label,
            "Environment": p.environment,
            "Last Deployed": p.last_deployed,
            "Status": p.status
        })
    
    df = pd.DataFrame(data)
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        env_filter = st.selectbox(
            "Filter by Environment",
            ["All"] + sorted(df["Environment"].unique().tolist())
        )
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All"] + sorted(df["Status"].unique().tolist())
        )
    
    # Apply filters
    if env_filter != "All":
        df = df[df["Environment"] == env_filter]
    if status_filter != "All":
        df = df[df["Status"] == status_filter]
    
    # Display dataframe with enhanced styling
    st.dataframe(
        df,
        column_config={
            "Name": st.column_config.TextColumn(
                "Name",
                help="Click to view prompt details",
                width="large"
            ),
            "Label": st.column_config.TextColumn(
                "Label",
                width="large"
            ),
            "Environment": st.column_config.TextColumn(
                "Environment",
                width="medium"
            ),
            "Last Deployed": st.column_config.DatetimeColumn(
                "Last Deployed",
                format="D MMM YYYY, HH:mm",
                width="medium"
            ),
            "Status": st.column_config.TextColumn(
                "Status",
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True
    )

def display_prompt_details(details) -> None:
    """Display prompt details with enhanced Streamlit styling."""
    if not details:
        st.warning("No details available for this prompt.")
        return
    
    # Header with status indicator
    status_color = "🟢" if details["status"] == "ACTIVE" else "🔴"
    st.header(f"{status_color} {details['name']}")
    
    # Basic Information
    st.subheader("ℹ️ Basic Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Environment", details["environment"])
    with col2:
        st.metric("Status", details["status"])
    with col3:
        st.metric("Model", details["model"])
    
    if details["description"]:
        st.info(details["description"])
    
    # Timestamps in a card-like container
    with st.container():
        st.subheader("⏰ Timestamps")
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            st.markdown(f"**Created:** {details['created'].strftime('%Y-%m-%d %H:%M:%S')}")
        with tcol2:
            st.markdown(f"**Last Deployed:** {details['last_deployed'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Input Variables
    if details["input_variables"]:
        st.subheader("🔑 Required Input Variables")
        for var in details["input_variables"]:
            st.code(var, language="python")
    
    # Version History
    if details["versions"]:
        st.subheader("📜 Version History")
        version_data = [{
            "Version": v["version"],
            "Created": v["created"],
            "Status": v["status"]
        } for v in details["versions"]]
        
        st.dataframe(
            pd.DataFrame(version_data),
            column_config={
                "Version": st.column_config.NumberColumn("Version", format="%d"),
                "Created": st.column_config.DatetimeColumn("Created", format="D MMM YYYY, HH:mm"),
                "Status": st.column_config.TextColumn("Status")
            },
            hide_index=True,
            use_container_width=True
        )

def execute_prompt_ui() -> None:
    """Display the prompt execution interface."""
    st.subheader("⚡ Execute Prompt")
    
    # Prompt selection
    prompts = st.session_state.explorer.list_prompts()
    prompt_names = [p.name for p in prompts]
    prompt_name = st.selectbox("Select Prompt", prompt_names)
    
    if prompt_name:
        details = st.session_state.explorer.get_prompt_details(prompt_name)
        if details and details["input_variables"]:
            st.markdown("##### Required Inputs")
            inputs_dict = {}
            
            # Create input fields for each required variable
            for var in details["input_variables"]:
                # Extract variable name from VellumVariable object or use as is if it's a string
                var_name = var.name if hasattr(var, 'name') else str(var)
                inputs_dict[var_name] = st.text_area(f"Enter {var_name}", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                stream_output = st.toggle("Stream Output", value=False)
            with col2:
                export_format = st.selectbox(
                    "Export Format",
                    ["None", "CSV", "XLSX", "JSON"]
                )
            
            if st.button("Execute Prompt", type="primary"):
                st.info("🔍 Debug Info:")
                st.code(f"""
Executing prompt with:
- Prompt Name: {prompt_name}
- Input Variables: {json.dumps({k: v for k, v in inputs_dict.items()}, indent=2)}
- Stream Output: {stream_output}
                """)
                
                with st.spinner("Executing prompt..."):
                    try:
                        # Log the exact state of inputs before execution
                        st.write("📤 Sending to Vellum:")
                        st.json({
                            "prompt_name": prompt_name,
                            "inputs": inputs_dict,
                            "stream": stream_output
                        })
                        
                        result = st.session_state.explorer.execute_prompt(
                            prompt_name=prompt_name,
                            inputs=inputs_dict,
                            stream=stream_output
                        )
                        
                        if result:
                            st.success("✅ Execution successful!")
                            st.write("📥 Received from Vellum:")
                            st.json(result)
                        else:
                            st.error("❌ Execution failed or returned no result.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        if hasattr(e, 'response') and hasattr(e.response, 'json'):
                            st.error("Response from Vellum:")
                            st.json(e.response.json())

# Main UI Layout
st.title("🔮 Vellum Prompt Explorer")

# Create tabs for different views
tab_help, tab_list, tab_execute = st.tabs([
    "📚 Help & Documentation",
    "📋 List Prompts",
    "⚡ Execute Prompt"
])

with tab_help:
    display_help()

with tab_list:
    st.header("Available Prompts")
    if st.button("🔄 Refresh Prompts", type="primary"):
        prompts = st.session_state.explorer.list_prompts()
        display_prompts(prompts)
    else:
        prompts = st.session_state.explorer.list_prompts()
        display_prompts(prompts)

with tab_execute:
    execute_prompt_ui() 