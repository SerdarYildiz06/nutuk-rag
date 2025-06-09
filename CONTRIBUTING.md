# Contributing to Nutuk RAG System

Thank you for your interest in contributing to the Nutuk RAG System! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. Check if the issue already exists
2. Provide a clear description of the problem
3. Include steps to reproduce the issue
4. Add relevant error messages or logs
5. Specify your environment (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please:

1. Check if the feature is already requested
2. Provide a clear description of the feature
3. Explain the use case and benefits
4. Consider implementation complexity

### Code Contributions

#### Development Setup

1. Fork the repository
2. Clone your fork:

   ```bash
   git clone https://github.com/SerdarYildiz06/nutuk-rag.git
   cd nutuk-rag
   ```

3. Create a virtual environment:

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Install Ollama and download models:
   ```bash
   ollama pull qwen2
   ```

#### Making Changes

1. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards
3. Test your changes thoroughly
4. Update documentation if needed

#### Testing

Before submitting:

1. Run the basic tests:

   ```bash
   python safe_interactive.py demo
   ```

2. Test the web interface:

   ```bash
   python improved_web_app.py
   ```

3. Run system comparison:
   ```bash
   python compare_systems.py
   ```

#### Submitting Changes

1. Commit your changes:

   ```bash
   git commit -m "Add: Brief description of your changes"
   ```

2. Push to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request with:
   - Clear title and description
   - Reference to related issues
   - Screenshots (for UI changes)
   - Test results

## 📋 Coding Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example:

```python
def search_documents(self, query: str, k: int = 6) -> List[Document]:
    """
    Search for relevant documents using hybrid search.

    Args:
        query: The search query string
        k: Number of documents to return

    Returns:
        List of relevant documents
    """
    # Implementation here
    pass
```

### Documentation

- Update README.md for user-facing changes
- Add inline comments for complex logic
- Update docstrings for API changes
- Include examples in documentation

### Commit Messages

Use clear, descriptive commit messages:

- `Add: New feature or functionality`
- `Fix: Bug fixes`
- `Update: Improvements to existing features`
- `Docs: Documentation changes`
- `Test: Adding or updating tests`

## 🔧 Areas for Contribution

### High Priority

- **Performance Optimization**: Improve search speed and accuracy
- **Multi-language Support**: Add support for other languages
- **Model Integration**: Support for more LLM models
- **UI/UX Improvements**: Enhance web interface

### Medium Priority

- **Documentation**: Improve guides and examples
- **Testing**: Add comprehensive test suite
- **Monitoring**: Add performance metrics
- **Configuration**: Better configuration management

### Ideas for New Features

- **Chat History**: Save conversation history
- **Export Options**: Export Q&A to different formats
- **Advanced Search**: More search filters and options
- **Analytics**: Usage statistics and insights
- **API Endpoints**: RESTful API for integration

## 🧪 Testing Guidelines

### Manual Testing

1. Test both original and improved systems
2. Try various question types
3. Check source attribution accuracy
4. Test edge cases and error handling

### Adding Tests

- Add tests for new features
- Test error conditions
- Include performance benchmarks
- Document test procedures

## 📞 Getting Help

If you need help:

1. Check existing documentation
2. Search closed issues for solutions
3. Create a new issue with your question
4. Join our community discussions

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes for significant contributions
- Project documentation

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Nutuk RAG System! 🙏
