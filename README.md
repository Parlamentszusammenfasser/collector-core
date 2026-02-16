# collector-core

Core library for collectors/scrapers of [PaZuFa](https://github.com/Chrystalkey/landtagszusammenfasser), providing shared functionality and base classes.

## Requirements

- Python 3.12+

## Installation

Install using Poetry:

```bash
poetry add collector-core
# or
poetry add git+https://github.com/Parlamentszusammenfasser/collector-core.git
```

Or with pip:

```bash
pip install collector-core
# or for local dev
pip install -e .
```

## Usage

```python
import collector_core
```

## Development

This project uses Poetry for dependency management.

### Setup

```bash
# Install dependencies
poetry install --with dev

# Run formatting and tests
poetry run isort .
poetry run black .
poetry run pytest

# to update API model
poetry run datamodel-codegen
```

## License

TBD
