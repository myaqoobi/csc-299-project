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

## 📋 Prerequisites

- Python 3.7 or higher
- pytest (for running tests)

## 🔧 Installation

1. Navigate to the tasks2 directory:
   ```bash
   cd tasks2
   ```

2. Install pytest (if not already installed):
   ```bash
   pip install pytest
   ```

## 📖 Usage

### Add a Task
```bash
python3 task_manager.py add "Finish project" "Complete all tasks" high --tags "work,urgent" --project "CSC299" --due tomorrow
```

### List Tasks
```bash
python3 task_manager.py list
python3 task_manager.py list --overdue
python3 task_manager.py list --project "CSC299"
```

### Search Tasks
```bash
python3 task_manager.py search "urgent" --in tags
```

### Update Task
```bash
python3 task_manager.py update 1 --status completed
```

### View Statistics
```bash
python3 task_manager.py stats
```

## 🧪 Testing

Run tests:
```bash
pytest test_task_manager.py -v
```

## 📚 Documentation

For complete documentation, run:
```bash
python3 task_manager.py help
```

