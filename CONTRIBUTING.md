# Contributing to Outdoor Tracker

Thank you for considering contributing to Outdoor Tracker! This document outlines the process for contributing to the project.

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:

1. Check the [issues](https://github.com/htschan/outdoortracker/issues) to see if the problem has already been reported
2. If you're unable to find an open issue addressing the problem, open a new issue using the bug report template

When filing an issue, include as much information as possible:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Screenshots or error logs
- Environment details (OS, browser, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement issue:

1. Use a clear and descriptive title
2. Provide a step-by-step description of the suggested enhancement
3. Explain why this enhancement would be useful
4. Include mockups or examples if applicable

### Pull Requests

1. Fork the repository
2. Create a branch for your feature or bugfix (`git checkout -b feature/my-feature`)
3. Make your changes
4. Add or update tests as needed
5. Ensure the test suite passes
6. Update documentation if necessary
7. Commit your changes (`git commit -m 'Add some feature'`)
8. Push to the branch (`git push origin feature/my-feature`)
9. Create a new Pull Request

## Development Process

### Setting Up the Development Environment

1. Clone your fork of the repository
2. Follow the installation instructions in the [README](README.md#development-setup)

### Coding Standards

#### Backend (Python)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use docstrings for functions, classes, and modules
- Write unit tests for new functionality

#### Frontend (Vue.js)

- Follow the [Vue.js Style Guide](https://vuejs.org/style-guide/)
- Use the project's ESLint configuration
- Prefer composition API over options API for new components

### Testing

- Write tests for new features and bug fixes
- Run existing tests before submitting a pull request
- Ensure your changes don't break existing functionality

### Documentation

- Update documentation when you change code behavior
- Document new features, options, or requirements
- Use clear, concise language

### Commit Messages

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

## License

By contributing to Outdoor Tracker, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
