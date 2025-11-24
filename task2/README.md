# Task 2 - Enhanced Task Manager

**What is this?**  
An upgraded version of Task 1 with Notion-inspired features like tags, projects, due dates, and bulk operations.

**New features:**
- 🏷️ Tags and categories
- 📁 Projects/workspaces
- 📅 Due dates (tomorrow, +3d, +2w, etc.)
- 🔄 Bulk update/delete
- 🔍 Advanced filtering
- 📊 Rich statistics

**How to use it:**
```bash
# Add task with tags and due date
python3 task_manager.py add "Finish project" high --tags "work,urgent" --project "CSC299" --due tomorrow

# List overdue tasks
python3 task_manager.py list --overdue

# Search in tags
python3 task_manager.py search "urgent" --in tags

# View stats
python3 task_manager.py stats
```

**Requirements:** Python 3.7+ (pytest for tests)

Run `python3 task_manager.py help` for full command list.
