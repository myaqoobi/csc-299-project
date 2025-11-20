# CSC299 Final Project – Personal Task Management System

This repository contains a Personal Knowledge Management System (PKMS) with task management capabilities, developed through multiple prototypes demonstrating iterative development, testing, AI integration, and specification-driven methodologies.

## Project Structure

The project consists of five distinct prototypes, each exploring different aspects of task management and development approaches:

1. **tasks1** – Basic CLI Prototype (Core functionality)
2. **tasks2** – Enhanced CLI with Tests (Feature expansion + testing)
3. **tasks3** – Properly Packaged Version (Professional structure with uv)
4. **tasks4** – AI Agent Experiment (OpenAI API integration)
5. **tasks5** – Spec-Driven Development Prototype (Web UI + specification methodology)

**Main Development Progression**: tasks1 → tasks2 → tasks3 represents the core terminal-based task management system that meets the assignment requirements.

---

## 1) Task 1 – Basic CLI Prototype

**Purpose**: Initial proof-of-concept establishing core task management functionality.

- **Folder**: `tasks1/`
- **Files**: `task_manager.py`, `README.md`
- **Storage**: `tasks.json` (auto-created when running)
- **Features**: Add, list, search, update, delete tasks; filter by status/priority; basic statistics

**Quick start:**
```bash
cd tasks1
python3 task_manager.py help
python3 task_manager.py add "Buy groceries" "Get milk and bread" high
python3 task_manager.py list
python3 task_manager.py stats
```

---

## 2) Task 2 – Enhanced CLI with Tests

**Purpose**: Expanded functionality with Notion-inspired features and comprehensive testing.

- **Folder**: `tasks2/`
- **Files**: `task_manager.py`, `test_task_manager.py`, `README.md`
- **Features**: 
  - Tags and projects for organization
  - Due dates with relative formats (tomorrow, +3d, +2w)
  - Advanced filtering (overdue, by project, by tag)
  - Bulk operations (update/delete multiple tasks)
  - Rich statistics and export functionality
  - Comprehensive pytest test suite

**Quick start:**
```bash
cd tasks2
python3 task_manager.py help
python3 task_manager.py add "Finish project" "Complete all tasks" high --tags "work,urgent" --project "CSC299" --due tomorrow
python3 task_manager.py list --overdue
pytest test_task_manager.py -v
```

**Common commands:**
```bash
# Search
python3 task_manager.py search "urgent" --in tags

# Update
python3 task_manager.py update 1 --status in_progress --priority high --due +3d

# Bulk operations
python3 task_manager.py bulk-update "1,2" completed
python3 task_manager.py bulk-delete "1,2"

# Organization
python3 task_manager.py stats
python3 task_manager.py projects
python3 task_manager.py tags
```

---

## 3) Task 3 – Properly Packaged Version

**Purpose**: Professional project structure using modern Python tooling (uv).

- **Folder**: `tasks3/`
- **Structure**: Proper Python package with `pyproject.toml`
- **Features**: Same as tasks2, but packaged for distribution
- **Testing**: Full pytest test suite included

**Quick start:**
```bash
cd tasks3
uv run tasks3  # Run the application
uv run pytest  # Run tests
```

**Requirements**: `uv` package manager (install from https://github.com/astral-sh/uv)

---

## 4) Task 4 – AI Agent Experiment

**Purpose**: Exploration of AI integration for task management using OpenAI API.

- **Folder**: `tasks4/`
- **Features**: AI-powered task summarization (paragraph → short phrase)
- **Technology**: OpenAI Chat Completions API (GPT-3.5-turbo)
- **Use Case**: Demonstrates how AI agents can enhance task management

**Quick start:**
```bash
cd tasks4
export OPENAI_API_KEY='your-api-key-here'
uv run tasks4
```

**Note**: This is a standalone experiment exploring AI capabilities, separate from the main task manager.

---

## 5) Task 5 – Spec-Driven Development Prototype

**Purpose**: Alternative development methodology using specification-first design.

- **Folder**: `tasks5/`
- **Type**: Web-based task manager (HTML/CSS/JavaScript)
- **Methodology**: Built using GitHub Spec Kit (spec-driven development)
- **Features**: Full-featured web UI with localStorage persistence
- **Documentation**: Complete specifications in `specs/001-task-manager/`

**Quick start:**
```bash
cd tasks5
# Open index.html in a web browser, or use a local server:
python3 -m http.server 8000
# Then open http://localhost:8000
```

**Note**: This prototype explores spec-driven development methodology and web-based interfaces. While it doesn't meet the terminal interface requirement, it demonstrates an alternative approach to the same problem.

---

## Repository Structure

```
.
├── tasks1/                    # Basic CLI prototype
│   ├── README.md
│   └── task_manager.py
├── tasks2/                    # Enhanced CLI with tests
│   ├── README.md
│   ├── task_manager.py
│   └── test_task_manager.py
├── tasks3/                    # Packaged version (uv)
│   ├── README.md
│   ├── pyproject.toml
│   ├── src/tasks3/
│   └── tests/
├── tasks4/                    # AI agent experiment
│   ├── README.md
│   ├── pyproject.toml
│   └── src/tasks4/
├── tasks5/                    # Spec-driven web prototype
│   ├── README.md
│   ├── index.html
│   ├── *.js, *.css
│   └── specs/
├── SUMMARY.md                 # Detailed development process documentation
├── video.txt                  # YouTube video URL (to be added)
└── README.md                  # This file
```

---

## Development Process

This project demonstrates:
- **Iterative Prototyping**: Multiple versions showing evolution of ideas
- **Test-Driven Development**: Comprehensive test suites in tasks2/3
- **AI-Assisted Development**: Built using Cursor AI and ChatGPT
- **Modern Python Tooling**: Package management with `uv`
- **AI Integration**: Exploration of OpenAI API for task enhancement
- **Spec-Driven Development**: Alternative methodology exploration

For detailed information about the development process, AI assistance modes used, what worked, and what didn't, see **`SUMMARY.md`** at the root of this repository.

---

## Deliverables

- ✅ Final version of software (tasks1-5)
- ✅ Fine-grained commit history showing development progression
- ✅ Multiple prototypes (tasks1-5)
- ✅ SUMMARY.md documenting development process
- ⏳ video.txt with YouTube demonstration URL (to be added before deadline)

---

## Requirements

- **Python 3.7+** for tasks1-4
- **uv** package manager for tasks3-4 (install from https://github.com/astral-sh/uv)
- **Modern web browser** for tasks5
- **OpenAI API key** (optional, for tasks4)

---

## Notes

- Tasks 1-3 are Python CLI apps, portable across Windows/macOS/Linux
- State is stored in JSON (`tasks.json`) for CLI apps, created automatically
- Tasks5 uses browser localStorage for persistence
- All prototypes are self-contained and can be run independently

For detailed feature lists and examples, see the README.md files in each task directory.

