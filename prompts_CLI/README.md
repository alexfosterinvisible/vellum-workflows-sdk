# Vellum Prompts CLI

A command-line interface tool for exploring and executing Vellum prompts, designed to help LLM developers quickly test and debug their prompts.

## Features

1. 🔍 **List Prompts** (90% complete)
   - View all available prompts in your Vellum workspace
   - Filter by status and environment
   - Rich console output with key details

2. 📋 **View Prompt Details** (80% complete)
   - Detailed information about specific prompts
   - Version history (coming soon)
   - Usage statistics (coming soon)

3. ▶️ **Execute Prompts** (95% complete)
   - Run prompts with custom inputs
   - JSON input support
   - Streaming support (coming soon)

4. 💾 **Result Management** (Planned)
   - Save execution results
   - Export results in various formats
   - Result caching for faster development

5. 🔧 **Diagnostics** (Planned)
   - Automated troubleshooting
   - Integration with learnings documentation
   - Performance optimization suggestions

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd prompts_CLI

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.template .env
# Edit .env with your Vellum API key
```

## Usage

```bash
# List all active prompts
vellum-explorer list

# View details of a specific prompt
vellum-explorer show <prompt-name>

# Execute a prompt with inputs
vellum-explorer execute <prompt-name> --inputs '{"key": "value"}'

# Get help
vellum-explorer --help
```

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src tests/

# Format code
black src/ tests/
```

## Project Structure

```
prompts_CLI/
├── src/
│   ├── __init__.py
│   ├── prompt_explorer.py  # Core functionality
│   └── cli.py             # CLI interface
├── tests/
│   └── test_prompt_explorer.py
├── requirements.txt
├── .env.template
└── README.md
```

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

[MIT License](LICENSE)

## Acknowledgments

- Built with [Vellum SDK](https://vellum.ai/docs)
- Uses [Rich](https://github.com/Textualize/rich) for beautiful console output
- Inspired by real-world LLM development needs 