# Contributing to Aisert

Thank you for your interest in contributing to Aisert! 🚀

## Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/aisert.git`
3. **Install** dependencies: `pip install -e .`
4. **Create** a branch: `git checkout -b feature/your-feature`
5. **Make** your changes
6. **Test** your changes: `python -m pytest`
7. **Submit** a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/haipad/aisert.git
cd aisert

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov black flake8
```

## Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=aisert

# Run specific test file
python -m pytest tests/test_aisert.py
```

## Code Style

- Use **Black** for code formatting: `black aisert/`
- Follow **PEP 8** guidelines
- Add **docstrings** to all public functions and classes
- Include **type hints** where appropriate

## What to Contribute

### 🐛 Bug Reports
- Use the bug report template
- Include minimal reproduction example
- Specify Python version and dependencies

### ✨ Feature Requests
- Use the feature request template
- Explain the use case and expected behavior
- Consider backward compatibility

### 🔧 Code Contributions
- **New Validators**: Extend validation capabilities
- **Provider Support**: Add new token counting providers
- **Performance**: Optimize existing functionality
- **Documentation**: Improve examples and guides
- **Tests**: Increase test coverage

## Pull Request Guidelines

1. **Small, focused changes** are preferred
2. **Update tests** for any new functionality
3. **Update documentation** if needed
4. **Follow existing code style**
5. **Write clear commit messages**

## Commit Message Format

```
type(scope): brief description

Longer explanation if needed

Fixes #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

## Areas for Contribution

### High Priority
- Additional token counting providers
- Performance optimizations
- Better error handling and logging
- Integration with popular testing frameworks

### Medium Priority
- Custom validation rules
- Batch processing improvements
- Memory usage optimizations
- Documentation improvements

### Future Ideas
- WebAssembly support for browser usage
- Custom model fine-tuning
- Enterprise features (audit logs, monitoring)
- Visual validation reporting

## Questions?

- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for sensitive topics

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to make AI validation better! 🤝

---

**Thank you for contributing to Aisert!** Every contribution, no matter how small, helps make the project better for everyone.