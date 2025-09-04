# Contributing to Rex AI Assistant 🤝

Thank you for your interest in contributing to Rex AI Assistant! This guide will help you get started with contributing to this professional AI productivity platform.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a professional and inclusive environment. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js (for PWA build tools)
- Git

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/[your-username]/ChatBot.git
   cd ChatBot
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Add your OpenRouter API key to .env
   ```

5. **Run Development Server**
   ```bash
   python main.py
   ```

## How to Contribute

### 🐛 Bug Reports
- Use the bug report template
- Include detailed reproduction steps
- Provide environment information
- Include screenshots for UI issues

### ✨ Feature Requests
- Use the feature request template
- Describe the problem you're solving
- Provide detailed requirements
- Consider implementation approach

### 🔧 Code Contributions
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes following our coding standards
3. Test your changes thoroughly
4. Update documentation as needed
5. Submit a pull request

## Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Maximum line length: 88 characters (Black formatter standard)

### JavaScript Code Style
- Use ES6+ modern JavaScript
- Follow consistent naming conventions
- Add comments for complex logic
- Use const/let instead of var

### HTML/CSS Standards
- Use semantic HTML5 elements
- Follow BEM methodology for CSS classes
- Ensure mobile-first responsive design
- Maintain accessibility standards (WCAG 2.1)

### Code Documentation
```python
def add_todo(todo: str, priority: str = "medium") -> dict:
    """
    Add a new todo item to the user's list.
    
    Args:
        todo (str): The task description
        priority (str): Task priority (low, medium, high, urgent)
    
    Returns:
        dict: Success status and todo details
    
    Raises:
        ValueError: If todo is empty or invalid priority
    """
```

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Commit Message Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semi-colons, etc)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```bash
feat(ai): add conversation memory functionality
fix(mobile): resolve touch gesture conflicts
docs(readme): update installation instructions
style(css): improve mobile responsiveness
refactor(storage): optimize data persistence layer
test(tools): add unit tests for todo management
chore(deps): update Flask to 3.1.2
```

## Pull Request Process

1. **Before Submitting**
   - [ ] Code follows project standards
   - [ ] All tests pass
   - [ ] Documentation updated
   - [ ] Self-review completed

2. **PR Template**
   - Use the provided PR template
   - Link related issues
   - Describe changes thoroughly
   - Include screenshots for UI changes

3. **Review Process**
   - Maintainer review required
   - Address feedback promptly
   - Keep PR focused and atomic
   - Squash commits before merge

## Testing Guidelines

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app tests/

# Run specific test file
python -m pytest tests/test_tools.py
```

### Writing Tests
- Write tests for new features
- Test edge cases and error conditions
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

## Development Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `fix/*`: Bug fixes
- `hotfix/*`: Critical production fixes

### Local Development
1. Create feature branch from `develop`
2. Implement changes with tests
3. Run quality checks locally
4. Submit PR to `develop` branch

## Questions and Support

- 📧 **Email**: [Maintainer Email]
- 💬 **Discussions**: Use GitHub Discussions
- 🐛 **Issues**: Create GitHub Issues
- 📖 **Documentation**: Check README.md

## Recognition

Contributors will be recognized in our README.md file and release notes. Thank you for helping make Rex AI Assistant better! 🚀

---

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.