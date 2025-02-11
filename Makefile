# ANSI color codes to match Rich output
BLUE := \033[38;2;122;162;247m
GREEN := \033[38;2;158;206;106m
PURPLE := \033[38;2;187;154;247m
CYAN := \033[38;2;125;207;255m
RESET := \033[0m
BOLD := \033[1m

.PHONY: help cli streamlit install

# Default target
help:
	@echo "$(PURPLE)$(BOLD)Vellum Prompt Explorer Commands:$(RESET)"
	@echo ""
	@echo "$(BOLD)Available commands:$(RESET)"
	@echo "  $(BLUE)make install$(RESET)    - Install required dependencies"
	@echo "  $(BLUE)make cli$(RESET)       - Run the CLI version"
	@echo "  $(BLUE)make streamlit$(RESET) - Run the Streamlit version"
	@echo "  $(BLUE)make help$(RESET)      - Show this help message"
	@echo ""
	@echo "$(CYAN)Examples:$(RESET)"
	@echo "  $$ make install"
	@echo "  $$ make cli"
	@echo "  $$ make streamlit"

# Install dependencies
install:
	@echo "$(PURPLE)Installing dependencies...$(RESET)"
	@pip install -r requirements.txt
	@pip install streamlit
	@echo "$(GREEN)✓ Dependencies installed successfully$(RESET)"

# Run the CLI version
cli:
	@echo "$(PURPLE)Starting CLI version...$(RESET)"
	@echo "$(CYAN)Type 'help' for available commands$(RESET)"
	@python prompts_CLI/src/prompt_explorer.py

# Run the Streamlit version
streamlit:
	@echo "$(PURPLE)Starting Streamlit version...$(RESET)"
	@echo "$(CYAN)The app will open in your default browser$(RESET)"
	@streamlit run prompts_CLI/src/prompt_explorer_streamlit.py

# Run both (for development)
dev: 
	@echo "$(PURPLE)Running both CLI and Streamlit versions...$(RESET)"
	@make cli
	@make streamlit 