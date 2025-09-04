# Contributing Guidelines Checklist

## Before Contributing
- [ ] Read [CONTRIBUTING.md](CONTRIBUTING.md) thoroughly
- [ ] Check existing issues and PRs to avoid duplicates
- [ ] Set up development environment correctly
- [ ] Ensure all tests pass locally

## Development Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] Environment variables configured (.env file)
- [ ] Pre-commit hooks installed (recommended)

## Code Quality Standards
- [ ] Code formatted with Black (line length: 88)
- [ ] Imports sorted with isort
- [ ] Linting passes with flake8
- [ ] Type hints added where appropriate
- [ ] Docstrings added for all functions and classes
- [ ] No security vulnerabilities (run bandit)

## Testing Requirements
- [ ] Unit tests written for new functionality
- [ ] All existing tests pass
- [ ] Test coverage maintained or improved
- [ ] Integration tests for API endpoints
- [ ] Manual testing completed on mobile and desktop

## Documentation Updates
- [ ] README.md updated if needed
- [ ] CHANGELOG.md updated with changes
- [ ] Code comments updated
- [ ] API documentation updated (if applicable)
- [ ] Screenshots updated (for UI changes)

## Commit Message Format
Use conventional commits format:
```
type(scope): description

[optional body]

[optional footer(s)]
```

Types: feat, fix, docs, style, refactor, test, chore

## Pull Request Checklist
- [ ] PR description clearly explains changes
- [ ] Links to related issues included
- [ ] Screenshots included for UI changes
- [ ] Breaking changes documented
- [ ] Backwards compatibility maintained
- [ ] Performance impact considered
- [ ] Security implications reviewed

## Deployment Readiness
- [ ] Works in production environment
- [ ] Environment variables properly configured
- [ ] Database migrations (if applicable)
- [ ] No hardcoded values or secrets
- [ ] Error handling comprehensive
- [ ] Logging appropriate