# Task 1 - Basic Task Manager

**What is this?**  
A simple command-line task manager that stores tasks in a JSON file. This is the prototype version.

**What can it do?**
- Add, list, search, update, and delete tasks
- Filter by status or priority
- View statistics

**How to use it:**
```bash
python3 task_manager.py add "Buy groceries" "Get milk and bread" high
python3 task_manager.py list
python3 task_manager.py search "groceries"
python3 task_manager.py update 1 completed
python3 task_manager.py stats
```

**Requirements:** Python 3.7+ (no extra packages needed)

Tasks are saved in `tasks.json` in this folder.
