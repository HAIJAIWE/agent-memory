# Contributing to Agent Memory System

Thank you for your interest in contributing! Here are some guidelines:

## Development Setup

```bash
git clone https://github.com/HAIJAIWE/agent-memory.git
cd agent-memory
pip install -r requirements.txt
```

## Making Changes

1. Create a new branch for your feature
2. Make your changes
3. Run tests: `pytest tests/`
4. Submit a pull request

## Code Style

We follow PEP 8. Use black for formatting:

```bash
black src/ tests/
```

## Testing

All new features should include tests. Run tests with:

```bash
pytest tests/ -v --cov=src
```

## Commit Messages

Use clear, descriptive commit messages:

```
Add feature X

Description of what this does and why.
```
