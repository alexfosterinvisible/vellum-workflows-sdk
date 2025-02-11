.PHONY: help cli streamlit install

# Default target
help:
	@echo "Available commands:"
	@echo "  make install    - Install required dependencies"
	@echo "  make cli       - Run the CLI version"
	@echo "  make streamlit - Run the Streamlit version"
	@echo "  make help      - Show this help message"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install streamlit

# Run the CLI version
cli:
	python prompts_CLI/src/prompt_explorer.py

# Run the Streamlit version
streamlit:
	streamlit run prompts_CLI/src/prompt_explorer_streamlit.py

# Run both (for development)
dev: cli streamlit 