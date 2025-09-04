# Contributing to Rex AI Assistant

Thank you for your interest in contributing to Rex AI Assistant! This document provides guidelines for contributing to this project.

## 🎯 Project Overview

Rex AI Assistant is an enterprise-grade AI productivity platform showcasing modern web development practices, mobile-first design, and advanced AI integration. We welcome contributions that improve the codebase, documentation, or user experience.

## 📋 How to Contribute

### 1. Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/ChatBot.git
   cd ChatBot
   ```
3. **Set up the development environment**:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Add your API keys to .env
   ```
4. **Run the application** to verify setup:
   ```bash
   python main.py
   ```

### 2. Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Commit with descriptive messages**:
   ```bash
   git commit -m "feat: add new productivity analytics feature"
   ```
5. **Push to your fork** and create a pull request

## 🔧 Development Guidelines

### Code Style

- **Python**: Follow PEP 8 standards
- **JavaScript**: Use ES6+ features and modern syntax
- **CSS**: Use consistent naming conventions and mobile-first approach
- **Comments**: Add clear, helpful comments for complex logic

### Mobile-First Development

- Always test on mobile devices and various screen sizes
- Ensure touch targets are at least 44px
- Test gesture interactions (swipe, tap, long press)
- Verify PWA functionality works correctly

### Performance Standards

- Maintain Lighthouse scores above 90 in all categories
- Optimize images and assets for fast loading
- Use efficient CSS and JavaScript patterns
- Test offline functionality

## 📝 Coding Standards

### Python Backend

```python
# Good: Clear function names and docstrings
def process_ai_message(message: str, user_context: dict) -> dict:
    """
    Process user message through AI API and return formatted response.
    
    Args:
        message: User input message
        user_context: Current user context and history
    
    Returns:
        dict: Formatted AI response with metadata
    """
    pass
```

### JavaScript Frontend

```javascript
// Good: Modern ES6+ syntax with clear intent
const handleUserInput = async (message) => {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        return await response.json();
    } catch (error) {
        console.error('Chat API error:', error);
        return { error: 'Failed to send message' };
    }
};
```

## 🧪 Testing

### Manual Testing

- Test on multiple devices (phone, tablet, desktop)
- Verify all touch interactions work properly
- Check PWA installation and offline functionality
- Test AI conversation features
- Validate todo list management

### Before Submitting

1. **Test mobile responsiveness** on different screen sizes
2. **Verify PWA functionality** (offline mode, installation)
3. **Check accessibility** (keyboard navigation, screen readers)
4. **Validate performance** (Lighthouse audit)
5. **Test error handling** (network failures, invalid inputs)

## 📤 Pull Request Process

### PR Requirements

1. **Clear description** of changes and motivation
2. **Screenshots** for UI changes (mobile and desktop)
3. **Testing notes** describing what was tested
4. **Performance impact** assessment if applicable

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update
- [ ] Mobile/PWA enhancement

## Testing
- [ ] Tested on mobile devices
- [ ] Verified PWA functionality
- [ ] Checked accessibility
- [ ] Performance audit completed

## Screenshots
[Add screenshots for UI changes]
```

## 🎯 Areas for Contribution

### High Priority

- **Mobile UX improvements** - gesture handling, animations
- **PWA enhancements** - offline capabilities, caching strategies
- **AI conversation features** - context awareness, smart responses
- **Accessibility improvements** - WCAG compliance, keyboard navigation
- **Performance optimizations** - bundle size, load times

### Documentation

- **Code comments** - explain complex algorithms and business logic
- **API documentation** - endpoint descriptions and examples
- **Setup guides** - deployment and development instructions
- **User guides** - feature explanations and best practices

### Testing

- **Cross-browser testing** - ensure compatibility across browsers
- **Device testing** - various phones, tablets, and screen sizes
- **Performance testing** - load times, memory usage, responsiveness
- **Accessibility testing** - screen readers, keyboard navigation

## 🤝 Community Guidelines

### Be Respectful

- Use inclusive language
- Be constructive in feedback
- Help newcomers learn and contribute
- Credit others for their work

### Communication

- **Issues**: Use clear, descriptive titles and provide reproduction steps
- **Discussions**: Stay on topic and be helpful
- **Reviews**: Provide actionable feedback with examples
- **Questions**: Check existing issues and documentation first

## 📚 Resources

### Technical Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Progressive Web Apps](https://web.dev/progressive-web-apps/)
- [Mobile Web Best Practices](https://developers.google.com/web/fundamentals/design-and-ux/principles)
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### Development Tools

- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Performance auditing
- [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools) - Mobile debugging
- [PWA Builder](https://www.pwabuilder.com/) - PWA testing and validation

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation credits

## 📞 Getting Help

- **Issues**: Create a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check existing documentation and guides

Thank you for contributing to Rex AI Assistant! 🚀