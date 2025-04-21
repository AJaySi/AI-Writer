# Contributing to AI-Writer

Thank you for your interest in contributing to AI-Writer! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## Getting Started

### Issues

- Check existing issues to see if your problem or idea has already been addressed.
- For bugs, create a new issue with a clear description, steps to reproduce, and relevant information about your environment.
- For feature requests, describe the feature, its benefits, and potential implementation approaches.
- Use issue templates when available.

### Feature Branches

- Fork the repository and create a feature branch from `main`.
- Use descriptive branch names: `feature/your-feature-name` or `fix/issue-description`.
- Keep branches focused on a single issue or feature.

## Development Environment

### Prerequisites

- Python 3.9 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)
- Docker (optional, for containerized development)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AJaySi/AI-Writer.git
   cd AI-Writer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add necessary API keys and configuration (see `.env.example` for reference)

5. Initialize the database:
   ```bash
   python -c "from lib.database.db_manager import init_db; init_db()"
   ```

6. Run the application:
   ```bash
   streamlit run alwrity.py
   ```

## Coding Standards

### Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Use 4 spaces for indentation (no tabs).
- Maximum line length is 100 characters.
- Use meaningful variable and function names.

### Documentation

- Use Google-style docstrings for all modules, classes, and functions.
- Include type hints in function signatures.
- Keep comments up-to-date with code changes.

Example:

```python
def generate_content(prompt: str, max_tokens: int = 100) -> str:
    """Generate content using the AI model.
    
    Args:
        prompt: The input prompt for content generation.
        max_tokens: Maximum number of tokens to generate.
        
    Returns:
        The generated content as a string.
        
    Raises:
        ValueError: If the prompt is empty or max_tokens is negative.
    """
    # Implementation...
```

### Error Handling

- Use specific exception types rather than generic exceptions.
- Include meaningful error messages.
- Log exceptions with appropriate context.

### Imports

- Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Within each group, imports should be sorted alphabetically.

## Pull Request Process

1. Ensure your code follows the project's coding standards.
2. Update documentation as necessary.
3. Add or update tests to cover your changes.
4. Ensure all tests pass.
5. Submit a pull request with a clear description of the changes and any relevant issue numbers.
6. Wait for review and address any feedback.

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or updating tests
- `chore`: Changes to the build process or auxiliary tools

Example: `feat: add support for Google Gemini models`

## Testing Guidelines

### Writing Tests

- Write unit tests for all new functions and classes.
- Place tests in the `tests/` directory, mirroring the package structure.
- Use descriptive test names that explain what is being tested.
- Aim for at least 80% test coverage for new code.

### Running Tests

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/path/to/test_file.py

# Run with coverage
pytest --cov=lib
```

## Documentation

### Code Documentation

- Document all public modules, classes, and functions.
- Keep docstrings up-to-date with code changes.
- Use type hints consistently.

### Project Documentation

- Update README.md with new features or changes.
- Update installation and usage instructions as needed.
- For significant changes, update the documentation in the `docs/` directory.

## Community

### Communication Channels

- GitHub Issues: For bug reports and feature requests
- Discussions: For general questions and discussions
- Pull Requests: For code contributions

### Recognition

All contributors will be recognized in the project's CONTRIBUTORS.md file.

## Additional Resources

- [Project Roadmap](docs/roadmap.rst)
- [Architecture Documentation](docs/architecture/index.rst)
- [API Reference](docs/api/index.rst)

Thank you for contributing to AI-Writer!