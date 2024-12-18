# PI SDK

Python SDK for interacting with the PI API.

## Installation

```bash
pip install pi-sdk
```

## Quick Start

```python
from pi_sdk import PIClient

# Initialize client
client = PIClient(api_key="your-api-key")

# Use the client
# ... examples to come
```

## Features

- Modern async/sync API support
- Type hints throughout
- Comprehensive error handling
- Automatic retries
- Rate limiting
- Streaming support
- Detailed logging

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/alexfosterinvisible/pi-sdk.git
cd pi-sdk
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run tests:
```bash
pytest
```

## Project Structure

```
pi_sdk/
├── src/
│   └── pi_sdk/
│       ├── __init__.py
│       ├── client.py      # Main client implementation
│       ├── exceptions.py  # Custom exceptions
│       └── models.py      # Pydantic models
├── tests/
│   ├── __init__.py
│   └── test_client.py
├── docs/
├── README.md
├── requirements.txt
└── setup.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
