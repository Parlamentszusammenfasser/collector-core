# collector-core

Core library for collecting parliamentary data.

## Installation

Install using Poetry:

```bash
poetry add collector-core
```

Or with pip:

```bash
pip install collector-core
```

## Usage

```python
from collector_core.collector import Collector

# Create a collector instance
collector = Collector(name="example")

# Collect data
data = collector.collect()
print(data)
```

## Development

This project uses Poetry for dependency management.

### Setup

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest
```

## License

TBD