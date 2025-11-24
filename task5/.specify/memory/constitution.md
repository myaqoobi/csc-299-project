# Task Manager Constitution

## Core Principles

### I. Simplicity First
The task manager is a learning project for CSC299. Every feature and implementation choice must prioritize clarity and educational value over complexity. Code should be easy to understand, modify, and extend. Avoid over-engineering - start with the simplest solution that works.

### II. User-Centric Design
The application must be intuitive and require minimal learning curve. Users should be able to manage their tasks effectively without consulting documentation. Clear visual feedback, helpful error messages, and logical workflows are mandatory.

### III. Data Persistence
All task data must be persisted reliably. Whether using files, databases, or local storage, data integrity is non-negotiable. Users must never lose their tasks due to application errors or crashes.

### IV. Testing & Quality
Code should be testable and include appropriate test coverage. While this is an educational project, following testing best practices prepares students for professional development. Tests should be clear, focused, and actually validate functionality.

### V. Modern Web Standards
When building web interfaces, use modern web standards and progressive enhancement. The application should work without JavaScript where possible, and enhance the experience when JavaScript is available. Prefer vanilla JavaScript and CSS over heavy frameworks unless there's a compelling reason.

## Development Constraints

### Technology Choices
- **Language**: Python for CLI/backend, JavaScript for web frontend
- **Data Storage**: JSON files for simple implementations, SQLite for more complex needs, localStorage for web apps
- **Dependencies**: Minimize external dependencies - prefer standard library when possible
- **Testing**: Use pytest for Python, built-in test frameworks for JavaScript

### Code Quality Standards
- Clear variable and function names
- Comments for complex logic, not obvious code
- Consistent formatting and style
- Error handling for user-facing operations
- Input validation for all user inputs

## Feature Requirements

### Core Features (Must Have)
1. Add, view, update, and delete tasks
2. Mark tasks as complete/incomplete
3. Data persistence across sessions
4. Basic task filtering and search

### Extended Features (Nice to Have)
4. Task priorities
5. Due dates
6. Tags and categories
7. Task statistics
8. Export capabilities

## Governance

This constitution guides all technical decisions for the task manager project. When making implementation choices:
1. Refer to Core Principles first
2. Consider the educational context
3. Choose clarity over cleverness
4. Document deviations with justification

**Version**: 1.0.0 | **Ratified**: 2025-11-18 | **Last Amended**: 2025-11-18
