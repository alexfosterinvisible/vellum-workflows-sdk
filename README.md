# Vellum Workflows SDK

A Python SDK and CLI tool for managing and executing Vellum prompts with advanced features and best practices.

## Features

1. **Prompt Management**
   - List available prompts with filtering
   - View detailed prompt information
   - Execute prompts with input validation
   - Stream prompt execution results

2. **CLI Interface**
   - Interactive command-line interface
   - Rich text output and formatting
   - Export functionality (CSV/XLSX/JSON)
   - Natural language documentation queries

3. **Advanced Features**
   - Parallel prompt execution
   - Rate limiting and error handling
   - Environment-based configuration
   - Detailed logging and diagnostics

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the CLI
python -m prompts_CLI.src.cli --help
```

## CLI Commands

```bash
# List available prompts
vellum-explorer list --status ACTIVE --environment DEVELOPMENT

# View prompt details
vellum-explorer inspect my-prompt

# Execute a prompt
vellum-explorer execute my-prompt --inputs '{"var": "value"}'

# Stream execution results
vellum-explorer execute my-prompt --inputs '{"var": "value"}' --stream

# Export results
vellum-explorer list --export prompts.csv
vellum-explorer execute my-prompt --inputs '{"var": "value"}' --export results.xlsx

# Get help
vellum-explorer help streaming

# Ask documentation questions
vellum-explorer ask "How do I use environment variables?"

# Combined list and inspect
vellum-explorer list-and-inspect --status ACTIVE
```

## Documentation

- [Quick Reference](docs/learnings/1_quick_reference.md)
- [Technical Details](docs/learnings/2_technical_details.md)
- [Troubleshooting](docs/learnings/3_troubleshooting.md)

## Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linter
flake8 prompts_CLI/

# Format code
autopep8 --in-place --recursive --aggressive --aggressive .
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Vellum](https://vellum.ai) - AI Prompt Management Platform
- Uses [OpenAI](https://openai.com) for natural language documentation queries
- Rich text interface powered by [Rich](https://github.com/Textualize/rich) 