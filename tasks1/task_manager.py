#!/usr/bin/env python3
"""
Command-line Task Management Application
CSC299 Project - Prototype Task Manager

This application allows users to store, list, and search tasks stored in a JSON data file.
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional


class TaskManager:
    """A simple task management system that stores tasks in a JSON file."""
    
    def __init__(self, data_file: str = "tasks.json"):
        """Initialize the TaskManager with a data file path."""
        self.data_file = data_file
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from the JSON file. Create file if it doesn't exist."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading tasks: {e}")
                return []
        else:
            # Create empty tasks file
            self._save_tasks([])
            return []
    
    def _save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Save tasks to the JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> None:
        """Add a new task to the list."""
        if not title.strip():
            print("Error: Task title cannot be empty.")
            return
        
        # Validate priority
        valid_priorities = ["low", "medium", "high"]
        if priority.lower() not in valid_priorities:
            print(f"Error: Priority must be one of {valid_priorities}")
            return
        
        task = {
            "id": len(self.tasks) + 1,
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority.lower(),
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.tasks.append(task)
        self._save_tasks(self.tasks)
        print(f"Task added successfully: '{title}'")
    
    def list_tasks(self, status_filter: Optional[str] = None, priority_filter: Optional[str] = None) -> None:
        """List all tasks with optional filtering."""
        if not self.tasks:
            print("No tasks found.")
            return
        
        filtered_tasks = self.tasks
        
        # Apply status filter
        if status_filter:
            valid_statuses = ["pending", "completed", "in_progress"]
            if status_filter.lower() not in valid_statuses:
                print(f"Error: Status must be one of {valid_statuses}")
                return
            filtered_tasks = [task for task in filtered_tasks if task["status"] == status_filter.lower()]
        
        # Apply priority filter
        if priority_filter:
            valid_priorities = ["low", "medium", "high"]
            if priority_filter.lower() not in valid_priorities:
                print(f"Error: Priority must be one of {valid_priorities}")
                return
            filtered_tasks = [task for task in filtered_tasks if task["priority"] == priority_filter.lower()]
        
        if not filtered_tasks:
            print("No tasks match the specified filters.")
            return
        
        print(f"\n{'='*80}")
        print(f"TASK LIST ({len(filtered_tasks)} task{'s' if len(filtered_tasks) != 1 else ''})")
        print(f"{'='*80}")
        
        for task in filtered_tasks:
            self._print_task(task)
    
    def _print_task(self, task: Dict[str, Any]) -> None:
        """Print a single task in a formatted way."""
        status_icon = {
            "pending": "⏳",
            "in_progress": "🔄", 
            "completed": "✅"
        }.get(task["status"], "❓")
        
        priority_icon = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴"
        }.get(task["priority"], "⚪")
        
        print(f"\nID: {task['id']}")
        print(f"Title: {task['title']}")
        if task['description']:
            print(f"Description: {task['description']}")
        print(f"Status: {status_icon} {task['status'].title()}")
        print(f"Priority: {priority_icon} {task['priority'].title()}")
        print(f"Created: {task['created_at'][:19].replace('T', ' ')}")
        print(f"Updated: {task['updated_at'][:19].replace('T', ' ')}")
        print("-" * 40)
    
    def search_tasks(self, query: str) -> None:
        """Search tasks by title or description."""
        if not query.strip():
            print("Error: Search query cannot be empty.")
            return
        
        query_lower = query.lower()
        matching_tasks = []
        
        for task in self.tasks:
            if (query_lower in task["title"].lower() or 
                query_lower in task["description"].lower()):
                matching_tasks.append(task)
        
        if not matching_tasks:
            print(f"No tasks found matching '{query}'.")
            return
        
        print(f"\n{'='*80}")
        print(f"SEARCH RESULTS for '{query}' ({len(matching_tasks)} task{'s' if len(matching_tasks) != 1 else ''})")
        print(f"{'='*80}")
        
        for task in matching_tasks:
            self._print_task(task)
    
    def update_task_status(self, task_id: int, new_status: str) -> None:
        """Update the status of a task."""
        valid_statuses = ["pending", "in_progress", "completed"]
        if new_status.lower() not in valid_statuses:
            print(f"Error: Status must be one of {valid_statuses}")
            return
        
        for task in self.tasks:
            if task["id"] == task_id:
                old_status = task["status"]
                task["status"] = new_status.lower()
                task["updated_at"] = datetime.now().isoformat()
                self._save_tasks(self.tasks)
                print(f"Task {task_id} status updated from '{old_status}' to '{new_status}'")
                return
        
        print(f"Task with ID {task_id} not found.")
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID."""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted_task = self.tasks.pop(i)
                self._save_tasks(self.tasks)
                print(f"Task deleted: '{deleted_task['title']}'")
                return
        
        print(f"Task with ID {task_id} not found.")
    
    def get_statistics(self) -> None:
        """Display task statistics."""
        if not self.tasks:
            print("No tasks found.")
            return
        
        total_tasks = len(self.tasks)
        pending = len([t for t in self.tasks if t["status"] == "pending"])
        in_progress = len([t for t in self.tasks if t["status"] == "in_progress"])
        completed = len([t for t in self.tasks if t["status"] == "completed"])
        
        high_priority = len([t for t in self.tasks if t["priority"] == "high"])
        medium_priority = len([t for t in self.tasks if t["priority"] == "medium"])
        low_priority = len([t for t in self.tasks if t["priority"] == "low"])
        
        print(f"\n{'='*50}")
        print("TASK STATISTICS")
        print(f"{'='*50}")
        print(f"Total Tasks: {total_tasks}")
        print(f"Pending: {pending}")
        print(f"In Progress: {in_progress}")
        print(f"Completed: {completed}")
        print(f"\nPriority Breakdown:")
        print(f"High Priority: {high_priority}")
        print(f"Medium Priority: {medium_priority}")
        print(f"Low Priority: {low_priority}")
        
        if total_tasks > 0:
            completion_rate = (completed / total_tasks) * 100
            print(f"\nCompletion Rate: {completion_rate:.1f}%")


def print_help():
    """Print help information."""
    help_text = """
Task Manager - Command Line Interface

USAGE:
    python task_manager.py <command> [arguments]

COMMANDS:
    add <title> [description] [priority]    Add a new task
    list [status] [priority]                List all tasks (with optional filters)
    search <query>                          Search tasks by title or description
    update <id> <status>                    Update task status
    delete <id>                             Delete a task
    stats                                   Show task statistics
    help                                    Show this help message

EXAMPLES:
    python task_manager.py add "Buy groceries" "Get milk and bread" high
    python task_manager.py list
    python task_manager.py list pending
    python task_manager.py list completed high
    python task_manager.py search "groceries"
    python task_manager.py update 1 completed
    python task_manager.py delete 1
    python task_manager.py stats

STATUS VALUES: pending, in_progress, completed
PRIORITY VALUES: low, medium, high
"""
    print(help_text)


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Error: No command specified.")
        print("Use 'python task_manager.py help' for usage information.")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    task_manager = TaskManager()
    
    if command == "help":
        print_help()
    
    elif command == "add":
        if len(sys.argv) < 3:
            print("Error: Task title is required.")
            print("Usage: python task_manager.py add <title> [description] [priority]")
            sys.exit(1)
        
        title = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        priority = sys.argv[4] if len(sys.argv) > 4 else "medium"
        
        task_manager.add_task(title, description, priority)
    
    elif command == "list":
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        priority_filter = sys.argv[3] if len(sys.argv) > 3 else None
        
        task_manager.list_tasks(status_filter, priority_filter)
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Search query is required.")
            print("Usage: python task_manager.py search <query>")
            sys.exit(1)
        
        query = " ".join(sys.argv[2:])
        task_manager.search_tasks(query)
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("Error: Task ID and status are required.")
            print("Usage: python task_manager.py update <id> <status>")
            sys.exit(1)
        
        try:
            task_id = int(sys.argv[2])
            new_status = sys.argv[3]
            task_manager.update_task_status(task_id, new_status)
        except ValueError:
            print("Error: Task ID must be a number.")
            sys.exit(1)
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Task ID is required.")
            print("Usage: python task_manager.py delete <id>")
            sys.exit(1)
        
        try:
            task_id = int(sys.argv[2])
            task_manager.delete_task(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
            sys.exit(1)
    
    elif command == "stats":
        task_manager.get_statistics()
    
    else:
        print(f"Error: Unknown command '{command}'.")
        print("Use 'python task_manager.py help' for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()

