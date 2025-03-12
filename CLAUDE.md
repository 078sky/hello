# Development Guide for Claude Code

## Commands
- **Frontend**
  - `cd frontend && npm start` - Start React development server
  - `cd frontend && npm test` - Run frontend tests (Jest)
  - `cd frontend && npm test -- --testNamePattern="specific test"` - Run specific test
  - `cd frontend && npm run build` - Build for production

- **Backend**
  - `cd backend && python app.py` - Start Flask server
  - `cd backend && python -m pytest` - Run all backend tests
  - `cd backend && python -m pytest tests/test_specific.py` - Run specific test
  - `cd backend && python -m flake8` - Lint Python code

## Code Style

### Python
- Use type annotations for function parameters and return values
- Handle exceptions with specific error types and descriptive messages
- Follow PEP 8 naming conventions (snake_case for functions/variables)
- Organize imports: stdlib, third-party, local modules
- Use comprehensive docstrings with parameters and return descriptions

### JavaScript/React
- Use ES6+ features and functional components
- Follow camelCase for variables/functions, PascalCase for components
- Import order: React, libraries, components, styles
- Prefer async/await over promise chains
- Use meaningful component and variable names

### Error Handling
- Log errors with appropriate level (debug, info, warning, error)
- Add context to errors when catching and re-raising
- Handle API errors gracefully with user-friendly messages