# Task Manager - Prototype

**CSC299 Project - Task 1**

A simple command-line task management application that stores tasks in a JSON file.

## Features

- Add tasks with title, description, and priority
- List all tasks or filter by status/priority
- Search tasks by keywords
- Update task status
- Delete tasks
- View task statistics

## Usage

### Add a Task
```bash
python3 task_manager.py add "Buy groceries" "Get milk and bread" high
```

### List Tasks
```bash
python3 task_manager.py list
python3 task_manager.py list pending
python3 task_manager.py list completed high
```

### Search Tasks
```bash
python3 task_manager.py search "groceries"
```

### Update Task Status
```bash
python3 task_manager.py update 1 completed
```

### Delete Task
```bash
python3 task_manager.py delete 1
```

### View Statistics
```bash
python3 task_manager.py stats
```

### Help
```bash
python3 task_manager.py help
```

## Requirements

- Python 3.7+
- No external dependencies required

## Data Storage

Tasks are stored in `tasks.json` in the same directory.

