# Enhanced Task Management System

**CSC299 Project - Task Manager with Notion-inspired Features**

A comprehensive command-line task management application with advanced features inspired by Notion, including tags, due dates, projects, bulk operations, and intelligent filtering.

## 🚀 Features

### Core Functionality
- ✅ **Add Tasks** - Create tasks with title, description, and priority
- ✅ **List Tasks** - View tasks with advanced filtering options
- ✅ **Search Tasks** - Search across titles, descriptions, tags, and projects
- ✅ **Update Tasks** - Modify task properties individually or in bulk
- ✅ **Delete Tasks** - Remove tasks individually or in bulk
- ✅ **Statistics** - Get comprehensive insights into your task data

### Notion-Inspired Enhancements
- 🏷️ **Tags/Categories** - Organize tasks with multiple tags
- 📁 **Projects** - Group tasks by project/workspace
- 📅 **Due Dates** - Set deadlines with flexible date formats
- 🔄 **Bulk Operations** - Update or delete multiple tasks at once
- 🔍 **Advanced Filtering** - Filter by status, priority, tags, projects, and dates
- 📊 **Rich Statistics** - View project breakdown, tag analysis, and due date tracking
- 📤 **Export Functionality** - Export all tasks to JSON

### Advanced Features
- ⏰ **Overdue Tracking** - Automatically identify overdue tasks
- 📆 **Date Management** - Support for relative dates (today, tomorrow, +3d, +2w, +1m)
- 🎯 **Smart Search** - Search in specific fields or across all fields
- 📈 **Completion Tracking** - Track when tasks were completed
- 🔄 **Status Management** - Three status levels: pending, in_progress, completed

## 📋 Prerequisites

- Python 3.7 or higher
- pytest (for running tests)

## 🔧 Installation

1. **Clone or navigate to the tasks2 directory:**
   ```bash
   cd tasks2
   ```

2. **Install pytest (if not already installed):**
   ```bash
   pip install pytest
   ```

3. **Run the application:**
   ```bash
   python task_manager.py help
   ```

## 📖 Usage

### Basic Commands

#### Add a Task
```bash
# Basic task
python task_manager.py add "Buy groceries" "Get milk and bread" high

# Task with tags
python task_manager.py add "Finish project" "Complete all tasks" high --tags "work,urgent"

# Task with project and due date
python task_manager.py add "Study for exam" "Review chapters 1-5" high --project "CSC299" --due tomorrow

# Task with all features
python task_manager.py add "Team meeting" "Discuss project progress" medium --tags "work,meeting" --project "Work" --due +3d
```

#### List Tasks
```bash
# List all tasks
python task_manager.py list

# Filter by status
python task_manager.py list pending
python task_manager.py list completed

# Filter by priority
python task_manager.py list high

# Combined filters
python task_manager.py list pending high

# Advanced filters
python task_manager.py list --overdue
python task_manager.py list --due-today
python task_manager.py list --due-week
python task_manager.py list --tag "urgent"
python task_manager.py list --project "CSC299"
```

#### Search Tasks
```bash
# Search in all fields
python task_manager.py search "groceries"

# Search in specific fields
python task_manager.py search "urgent" --in tags
python task_manager.py search "CSC299" --in project
python task_manager.py search "meeting" --in title
```

#### Update Tasks
```bash
# Update status
python task_manager.py update 1 --status completed

# Update multiple fields
python task_manager.py update 1 --title "New Title" --desc "New Description" --priority high

# Update with tags and due date
python task_manager.py update 1 --tags "work,urgent" --project "CSC299" --due +7d
```

#### Tag Management
```bash
# Add tags to a task
python task_manager.py add-tags 1 work urgent important

# Remove tags from a task
python task_manager.py remove-tags 1 urgent
```

#### Bulk Operations
```bash
# Update multiple tasks' status
python task_manager.py bulk-update "1,2,3" completed

# Delete multiple tasks
python task_manager.py bulk-delete "1,2,3"
```

#### Organization
```bash
# List all projects
python task_manager.py projects

# List all tags
python task_manager.py tags

# View statistics
python task_manager.py stats
```

#### Export
```bash
# Export to default filename
python task_manager.py export

# Export to specific file
python task_manager.py export my_tasks_backup.json
```

## 📅 Due Date Formats

The application supports multiple due date formats:

- **ISO Format**: `2025-12-31`
- **Relative Keywords**: `today`, `tomorrow`
- **Relative Days**: `+3d` (3 days from today), `+5d` (5 days)
- **Relative Weeks**: `+2w` (2 weeks from today), `+1w` (1 week)
- **Relative Months**: `+1m` (1 month from today), `+2m` (2 months)

Examples:
```bash
python task_manager.py add "Task 1" --due today
python task_manager.py add "Task 2" --due tomorrow
python task_manager.py add "Task 3" --due +3d
python task_manager.py add "Task 4" --due +2w
python task_manager.py add "Task 5" --due 2025-12-31
```

## 🧪 Testing

Run the test suite using pytest:

```bash
# Run all tests
pytest test_task_manager.py -v

# Run specific test
pytest test_task_manager.py::TestTaskManager::test_add_task_basic -v

# Run with coverage (if pytest-cov is installed)
pytest test_task_manager.py --cov=task_manager --cov-report=html
```

### Test Coverage

The test suite includes comprehensive tests for:
- ✅ Task creation with all features
- ✅ Task listing and filtering
- ✅ Task search functionality
- ✅ Task updates (individual fields and bulk)
- ✅ Tag management (add/remove)
- ✅ Bulk operations (update/delete)
- ✅ Due date parsing and validation
- ✅ Statistics and reporting
- ✅ Export functionality
- ✅ Edge cases and error handling

## 📊 Data Storage

Tasks are stored in a JSON file (`tasks.json` by default). The file format includes:

```json
[
  {
    "id": 1,
    "title": "Task Title",
    "description": "Task Description",
    "priority": "high",
    "status": "pending",
    "tags": ["work", "urgent"],
    "project": "CSC299",
    "due_date": "2025-12-31",
    "created_at": "2025-01-01T10:00:00",
    "updated_at": "2025-01-01T10:00:00",
    "completed_at": null
  }
]
```

## 🔄 Command Reference

### Core Commands
| Command | Description | Example |
|---------|-------------|---------|
| `add` | Add a new task | `add "Title" "Desc" high --tags "a,b" --project "P" --due tomorrow` |
| `list` | List tasks with filters | `list pending --tag "urgent" --overdue` |
| `search` | Search tasks | `search "query" --in tags` |
| `update` | Update task | `update 1 --status completed --priority high` |
| `delete` | Delete task | `delete 1` |
| `stats` | Show statistics | `stats` |

### Tag Management
| Command | Description | Example |
|---------|-------------|---------|
| `add-tags` | Add tags to task | `add-tags 1 tag1 tag2` |
| `remove-tags` | Remove tags from task | `remove-tags 1 tag1` |

### Bulk Operations
| Command | Description | Example |
|---------|-------------|---------|
| `bulk-update` | Update multiple tasks | `bulk-update "1,2,3" completed` |
| `bulk-delete` | Delete multiple tasks | `bulk-delete "1,2,3"` |

### Organization
| Command | Description | Example |
|---------|-------------|---------|
| `projects` | List all projects | `projects` |
| `tags` | List all tags | `tags` |
| `export` | Export tasks to JSON | `export backup.json` |

### Filter Flags for `list` Command
| Flag | Description | Example |
|------|-------------|---------|
| `--overdue` | Show only overdue tasks | `list --overdue` |
| `--due-today` | Show tasks due today | `list --due-today` |
| `--due-week` | Show tasks due this week | `list --due-week` |
| `--tag TAG` | Filter by tag | `list --tag "urgent"` |
| `--project PROJECT` | Filter by project | `list --project "CSC299"` |

## 📝 Examples

### Complete Workflow

```bash
# 1. Add several tasks with different properties
python task_manager.py add "Finish homework" "Complete chapter 5" high --tags "school,homework" --project "CSC299" --due tomorrow
python task_manager.py add "Buy groceries" "Milk, bread, eggs" medium --tags "shopping,personal" --due +2d
python task_manager.py add "Team meeting" "Weekly sync" low --tags "work,meeting" --project "Work" --due today

# 2. View all tasks
python task_manager.py list

# 3. Filter by project
python task_manager.py list --project "CSC299"

# 4. Check overdue tasks
python task_manager.py list --overdue

# 5. Search for urgent tasks
python task_manager.py search "urgent" --in tags

# 6. Update task status
python task_manager.py update 1 --status in_progress

# 7. Bulk complete multiple tasks
python task_manager.py bulk-update "1,2" completed

# 8. View statistics
python task_manager.py stats

# 9. List all projects
python task_manager.py projects

# 10. Export tasks
python task_manager.py export backup.json
```

## 🐛 Error Handling

The application includes comprehensive error handling:

- ✅ Validates task titles (cannot be empty)
- ✅ Validates priority values (low/medium/high)
- ✅ Validates status values (pending/in_progress/completed)
- ✅ Validates due date formats
- ✅ Handles missing tasks gracefully
- ✅ Provides helpful error messages

## 🎯 Design Philosophy

This task manager is inspired by Notion's flexibility and organization features:

- **Flexible Organization**: Tags and projects allow multiple organizational schemes
- **Smart Defaults**: Sensible defaults for priority and status
- **Relative Dates**: Human-friendly date formats like "tomorrow" and "+3d"
- **Bulk Operations**: Efficiency for managing multiple tasks
- **Rich Filtering**: Powerful filtering options for finding exactly what you need
- **Comprehensive Stats**: Insights into your task patterns

## 📚 Project Structure

```
tasks2/
├── task_manager.py      # Main application code
├── test_task_manager.py  # Test suite
├── README.md            # This file
└── tasks.json           # Data file (created automatically)
```

## 🤝 Contributing

This is a class project for CSC299. For improvements:

1. Add new features following existing patterns
2. Write tests for new functionality
3. Update this README with new commands/features
4. Maintain code quality and documentation

## 📄 License

This project is for educational purposes as part of CSC299 course work.

## 🙏 Acknowledgments

- Inspired by Notion's task management features
- Built with Python 3 and pytest
- Designed for portability across Windows, macOS, and Linux

---

**Version**: 2.0  
**Last Updated**: 2025-01-01  
**Python Version**: 3.7+

