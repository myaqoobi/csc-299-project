#!/usr/bin/env python3
"""
Enhanced Task Management Application
CSC299 Project - Task Manager with Notion-inspired Features

This application allows users to store, list, search, and manage tasks with advanced features
inspired by Notion, including tags, due dates, projects, and bulk operations.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict


class TaskManager:
    """An enhanced task management system with Notion-inspired features."""
    
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
    
    def _get_next_id(self) -> int:
        """Get the next available task ID."""
        if not self.tasks:
            return 1
        return max(task.get("id", 0) for task in self.tasks) + 1
    
    def add_task(
        self, 
        title: str, 
        description: str = "", 
        priority: str = "medium",
        tags: Optional[List[str]] = None,
        project: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> bool:
        """
        Add a new task to the list with enhanced features.
        
        Args:
            title: Task title (required)
            description: Task description
            priority: Priority level (low/medium/high)
            tags: List of tags/categories
            project: Project/workspace name
            due_date: Due date in ISO format (YYYY-MM-DD) or relative format (e.g., "tomorrow", "+3d")
        
        Returns:
            True if task was added successfully, False otherwise
        """
        if not title.strip():
            print("Error: Task title cannot be empty.")
            return False
        
        # Validate priority
        valid_priorities = ["low", "medium", "high"]
        if priority.lower() not in valid_priorities:
            print(f"Error: Priority must be one of {valid_priorities}")
            return False
        
        # Parse due date
        parsed_due_date = self._parse_due_date(due_date) if due_date else None
        
        # Validate due date format
        if parsed_due_date and not self._validate_date(parsed_due_date):
            print("Error: Invalid due date format. Use YYYY-MM-DD or relative format (tomorrow, +3d, etc.)")
            return False
        
        task = {
            "id": self._get_next_id(),
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority.lower(),
            "status": "pending",
            "tags": [tag.strip() for tag in (tags or [])] if tags else [],
            "project": project.strip() if project else None,
            "due_date": parsed_due_date,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.tasks.append(task)
        self._save_tasks(self.tasks)
        print(f"✓ Task added successfully: '{title}' (ID: {task['id']})")
        return True
    
    def _parse_due_date(self, due_date: str) -> Optional[str]:
        """Parse relative date formats like 'tomorrow', '+3d', '+1w'."""
        due_date = due_date.strip().lower()
        
        today = datetime.now().date()
        
        # Handle relative dates
        if due_date == "today":
            return today.isoformat()
        elif due_date == "tomorrow" or due_date == "+1d":
            return (today + timedelta(days=1)).isoformat()
        elif due_date.startswith("+"):
            # Parse formats like +3d, +2w, +1m
            try:
                if due_date.endswith("d"):
                    days = int(due_date[1:-1])
                    return (today + timedelta(days=days)).isoformat()
                elif due_date.endswith("w"):
                    weeks = int(due_date[1:-1])
                    return (today + timedelta(weeks=weeks)).isoformat()
                elif due_date.endswith("m"):
                    months = int(due_date[1:-1])
                    # Approximate: 30 days per month
                    return (today + timedelta(days=months * 30)).isoformat()
            except ValueError:
                pass
        
        # Try to parse as ISO date (YYYY-MM-DD)
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            return due_date
        except ValueError:
            pass
        
        return None
    
    def _validate_date(self, date_str: str) -> bool:
        """Validate date string format."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def list_tasks(
        self, 
        status_filter: Optional[str] = None, 
        priority_filter: Optional[str] = None,
        tag_filter: Optional[str] = None,
        project_filter: Optional[str] = None,
        overdue_only: bool = False,
        due_today: bool = False,
        due_this_week: bool = False
    ) -> None:
        """List all tasks with advanced filtering options."""
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
            filtered_tasks = [task for task in filtered_tasks if task.get("priority") == priority_filter.lower()]
        
        # Apply tag filter
        if tag_filter:
            filtered_tasks = [
                task for task in filtered_tasks 
                if tag_filter.lower() in [tag.lower() for tag in task.get("tags", [])]
            ]
        
        # Apply project filter
        if project_filter:
            filtered_tasks = [
                task for task in filtered_tasks 
                if task.get("project") and project_filter.lower() in task.get("project", "").lower()
            ]
        
        # Apply date filters
        today = datetime.now().date()
        
        if overdue_only:
            filtered_tasks = [
                task for task in filtered_tasks
                if task.get("due_date") 
                and datetime.strptime(task["due_date"], "%Y-%m-%d").date() < today
                and task.get("status") != "completed"
            ]
        
        if due_today:
            filtered_tasks = [
                task for task in filtered_tasks
                if task.get("due_date")
                and datetime.strptime(task["due_date"], "%Y-%m-%d").date() == today
            ]
        
        if due_this_week:
            week_end = today + timedelta(days=7)
            filtered_tasks = [
                task for task in filtered_tasks
                if task.get("due_date")
                and today <= datetime.strptime(task["due_date"], "%Y-%m-%d").date() <= week_end
            ]
        
        if not filtered_tasks:
            print("No tasks match the specified filters.")
            return
        
        print(f"\n{'='*80}")
        print(f"TASK LIST ({len(filtered_tasks)} task{'s' if len(filtered_tasks) != 1 else ''})")
        print(f"{'='*80}")
        
        for task in filtered_tasks:
            self._print_task(task)
    
    def _print_task(self, task: Dict[str, Any]) -> None:
        """Print a single task in a formatted way with enhanced information."""
        status_icon = {
            "pending": "⏳",
            "in_progress": "🔄", 
            "completed": "✅"
        }.get(task.get("status"), "❓")
        
        priority_icon = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴"
        }.get(task.get("priority"), "⚪")
        
        print(f"\nID: {task['id']}")
        print(f"Title: {task['title']}")
        
        if task.get("description"):
            print(f"Description: {task['description']}")
        
        print(f"Status: {status_icon} {task.get('status', 'pending').title()}")
        print(f"Priority: {priority_icon} {task.get('priority', 'medium').title()}")
        
        if task.get("tags"):
            print(f"Tags: {', '.join(task['tags'])}")
        
        if task.get("project"):
            print(f"Project: 📁 {task['project']}")
        
        if task.get("due_date"):
            due_date_obj = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            today = datetime.now().date()
            
            if due_date_obj < today and task.get("status") != "completed":
                print(f"Due Date: 🔴 {task['due_date']} (OVERDUE)")
            elif due_date_obj == today:
                print(f"Due Date: 🟡 {task['due_date']} (TODAY)")
            else:
                days_until = (due_date_obj - today).days
                print(f"Due Date: 📅 {task['due_date']} ({days_until} days)")
        
        print(f"Created: {task['created_at'][:19].replace('T', ' ')}")
        print(f"Updated: {task['updated_at'][:19].replace('T', ' ')}")
        
        if task.get("completed_at"):
            print(f"Completed: {task['completed_at'][:19].replace('T', ' ')}")
        
        print("-" * 40)
    
    def search_tasks(self, query: str, search_in: str = "all") -> None:
        """
        Advanced search tasks by title, description, tags, or project.
        
        Args:
            query: Search query
            search_in: Where to search - "all", "title", "description", "tags", "project"
        """
        if not query.strip():
            print("Error: Search query cannot be empty.")
            return
        
        query_lower = query.lower()
        matching_tasks = []
        
        for task in self.tasks:
            match = False
            
            if search_in == "all" or search_in == "title":
                if query_lower in task.get("title", "").lower():
                    match = True
            
            if search_in == "all" or search_in == "description":
                if query_lower in task.get("description", "").lower():
                    match = True
            
            if search_in == "all" or search_in == "tags":
                for tag in task.get("tags", []):
                    if query_lower in tag.lower():
                        match = True
                        break
            
            if search_in == "all" or search_in == "project":
                if task.get("project") and query_lower in task.get("project", "").lower():
                    match = True
            
            if match:
                matching_tasks.append(task)
        
        if not matching_tasks:
            print(f"No tasks found matching '{query}'.")
            return
        
        print(f"\n{'='*80}")
        print(f"SEARCH RESULTS for '{query}' ({len(matching_tasks)} task{'s' if len(matching_tasks) != 1 else ''})")
        print(f"{'='*80}")
        
        for task in matching_tasks:
            self._print_task(task)
    
    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        project: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> bool:
        """Update task properties with enhanced fields."""
        for task in self.tasks:
            if task["id"] == task_id:
                if title:
                    task["title"] = title.strip()
                if description is not None:
                    task["description"] = description.strip()
                if priority:
                    valid_priorities = ["low", "medium", "high"]
                    if priority.lower() not in valid_priorities:
                        print(f"Error: Priority must be one of {valid_priorities}")
                        return False
                    task["priority"] = priority.lower()
                if status:
                    valid_statuses = ["pending", "in_progress", "completed"]
                    if status.lower() not in valid_statuses:
                        print(f"Error: Status must be one of {valid_statuses}")
                        return False
                    old_status = task["status"]
                    task["status"] = status.lower()
                    if status.lower() == "completed" and not task.get("completed_at"):
                        task["completed_at"] = datetime.now().isoformat()
                    elif status.lower() != "completed":
                        task["completed_at"] = None
                if tags is not None:
                    task["tags"] = [tag.strip() for tag in tags] if tags else []
                if project is not None:
                    task["project"] = project.strip() if project else None
                if due_date:
                    parsed_due_date = self._parse_due_date(due_date)
                    if not parsed_due_date or not self._validate_date(parsed_due_date):
                        print("Error: Invalid due date format.")
                        return False
                    task["due_date"] = parsed_due_date
                
                task["updated_at"] = datetime.now().isoformat()
                self._save_tasks(self.tasks)
                print(f"✓ Task {task_id} updated successfully")
                return True
        
        print(f"Task with ID {task_id} not found.")
        return False
    
    def add_tags(self, task_id: int, tags: List[str]) -> bool:
        """Add tags to an existing task."""
        for task in self.tasks:
            if task["id"] == task_id:
                existing_tags = set(task.get("tags", []))
                new_tags = [tag.strip() for tag in tags]
                task["tags"] = list(existing_tags.union(new_tags))
                task["updated_at"] = datetime.now().isoformat()
                self._save_tasks(self.tasks)
                print(f"✓ Tags added to task {task_id}")
                return True
        print(f"Task with ID {task_id} not found.")
        return False
    
    def remove_tags(self, task_id: int, tags: List[str]) -> bool:
        """Remove tags from an existing task."""
        for task in self.tasks:
            if task["id"] == task_id:
                existing_tags = set(task.get("tags", []))
                tags_to_remove = set(tag.strip().lower() for tag in tags)
                task["tags"] = [tag for tag in existing_tags if tag.lower() not in tags_to_remove]
                task["updated_at"] = datetime.now().isoformat()
                self._save_tasks(self.tasks)
                print(f"✓ Tags removed from task {task_id}")
                return True
        print(f"Task with ID {task_id} not found.")
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted_task = self.tasks.pop(i)
                self._save_tasks(self.tasks)
                print(f"✓ Task deleted: '{deleted_task['title']}'")
                return True
        
        print(f"Task with ID {task_id} not found.")
        return False
    
    def bulk_update_status(self, task_ids: List[int], new_status: str) -> int:
        """Update status of multiple tasks at once."""
        valid_statuses = ["pending", "in_progress", "completed"]
        if new_status.lower() not in valid_statuses:
            print(f"Error: Status must be one of {valid_statuses}")
            return 0
        
        updated_count = 0
        for task in self.tasks:
            if task["id"] in task_ids:
                task["status"] = new_status.lower()
                if new_status.lower() == "completed" and not task.get("completed_at"):
                    task["completed_at"] = datetime.now().isoformat()
                elif new_status.lower() != "completed":
                    task["completed_at"] = None
                task["updated_at"] = datetime.now().isoformat()
                updated_count += 1
        
        if updated_count > 0:
            self._save_tasks(self.tasks)
            print(f"✓ Updated {updated_count} task(s) to '{new_status}'")
        
        return updated_count
    
    def bulk_delete(self, task_ids: List[int]) -> int:
        """Delete multiple tasks at once."""
        deleted_count = 0
        self.tasks = [task for task in self.tasks if task["id"] not in task_ids or (deleted_count := deleted_count + 1) == deleted_count]
        
        if deleted_count > 0:
            self._save_tasks(self.tasks)
            print(f"✓ Deleted {deleted_count} task(s)")
        
        return deleted_count
    
    def get_statistics(self) -> None:
        """Display enhanced task statistics with Notion-inspired insights."""
        if not self.tasks:
            print("No tasks found.")
            return
        
        total_tasks = len(self.tasks)
        pending = len([t for t in self.tasks if t.get("status") == "pending"])
        in_progress = len([t for t in self.tasks if t.get("status") == "in_progress"])
        completed = len([t for t in self.tasks if t.get("status") == "completed"])
        
        high_priority = len([t for t in self.tasks if t.get("priority") == "high"])
        medium_priority = len([t for t in self.tasks if t.get("priority") == "medium"])
        low_priority = len([t for t in self.tasks if t.get("priority") == "low"])
        
        # Project statistics
        projects = defaultdict(int)
        for task in self.tasks:
            if task.get("project"):
                projects[task["project"]] += 1
        
        # Tag statistics
        tags = defaultdict(int)
        for task in self.tasks:
            for tag in task.get("tags", []):
                tags[tag] += 1
        
        # Due date statistics
        today = datetime.now().date()
        overdue = len([
            t for t in self.tasks
            if t.get("due_date")
            and datetime.strptime(t["due_date"], "%Y-%m-%d").date() < today
            and t.get("status") != "completed"
        ])
        due_today = len([
            t for t in self.tasks
            if t.get("due_date")
            and datetime.strptime(t["due_date"], "%Y-%m-%d").date() == today
        ])
        due_this_week = len([
            t for t in self.tasks
            if t.get("due_date")
            and today <= datetime.strptime(t["due_date"], "%Y-%m-%d").date() <= today + timedelta(days=7)
        ])
        
        print(f"\n{'='*60}")
        print("📊 TASK STATISTICS")
        print(f"{'='*60}")
        print(f"\n📋 Overview:")
        print(f"  Total Tasks: {total_tasks}")
        print(f"  ⏳ Pending: {pending}")
        print(f"  🔄 In Progress: {in_progress}")
        print(f"  ✅ Completed: {completed}")
        
        print(f"\n🎯 Priority Breakdown:")
        print(f"  🔴 High Priority: {high_priority}")
        print(f"  🟡 Medium Priority: {medium_priority}")
        print(f"  🟢 Low Priority: {low_priority}")
        
        if total_tasks > 0:
            completion_rate = (completed / total_tasks) * 100
            print(f"\n📈 Completion Rate: {completion_rate:.1f}%")
        
        if projects:
            print(f"\n📁 Projects ({len(projects)}):")
            for project, count in sorted(projects.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  • {project}: {count} task(s)")
        
        if tags:
            print(f"\n🏷️  Top Tags ({len(tags)} total):")
            for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  • {tag}: {count} task(s)")
        
        if any(t.get("due_date") for t in self.tasks):
            print(f"\n📅 Due Dates:")
            print(f"  🔴 Overdue: {overdue}")
            print(f"  🟡 Due Today: {due_today}")
            print(f"  📆 Due This Week: {due_this_week}")
    
    def export_tasks(self, filename: Optional[str] = None) -> bool:
        """Export tasks to a JSON file."""
        if not filename:
            filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
            print(f"✓ Tasks exported to {filename}")
            return True
        except IOError as e:
            print(f"Error exporting tasks: {e}")
            return False
    
    def list_projects(self) -> None:
        """List all projects and their task counts."""
        projects = defaultdict(int)
        for task in self.tasks:
            if task.get("project"):
                projects[task["project"]] += 1
        
        if not projects:
            print("No projects found.")
            return
        
        print(f"\n{'='*60}")
        print(f"📁 PROJECTS ({len(projects)})")
        print(f"{'='*60}")
        for project, count in sorted(projects.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {project}: {count} task(s)")
    
    def list_tags(self) -> None:
        """List all tags and their task counts."""
        tags = defaultdict(int)
        for task in self.tasks:
            for tag in task.get("tags", []):
                tags[tag] += 1
        
        if not tags:
            print("No tags found.")
            return
        
        print(f"\n{'='*60}")
        print(f"🏷️  TAGS ({len(tags)})")
        print(f"{'='*60}")
        for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {tag}: {count} task(s)")


def print_help():
    """Print comprehensive help information."""
    help_text = """
Enhanced Task Manager - Command Line Interface
Inspired by Notion with advanced features

USAGE:
    python task_manager.py <command> [arguments]

CORE COMMANDS:
    add <title> [description] [priority] [--tags tag1,tag2] [--project PROJECT] [--due DATE]
        Add a new task with optional tags, project, and due date
        Due date formats: YYYY-MM-DD, "today", "tomorrow", "+3d", "+2w", "+1m"
    
    list [status] [priority] [--tag TAG] [--project PROJECT] [--overdue] [--due-today] [--due-week]
        List tasks with advanced filtering options
    
    search <query> [--in title|description|tags|project|all]
        Search tasks in specific fields or all fields
    
    update <id> [--title TITLE] [--desc DESCRIPTION] [--priority PRIORITY] 
              [--status STATUS] [--tags tag1,tag2] [--project PROJECT] [--due DATE]
        Update task properties
    
    delete <id>                    Delete a task by ID
    
    stats                          Show comprehensive task statistics

TAG MANAGEMENT:
    add-tags <id> tag1 tag2 ...   Add tags to a task
    remove-tags <id> tag1 tag2 ... Remove tags from a task

BULK OPERATIONS:
    bulk-update <id1,id2,...> <status>    Update multiple tasks' status
    bulk-delete <id1,id2,...>             Delete multiple tasks

ORGANIZATION:
    projects                     List all projects
    tags                         List all tags
    
EXPORT:
    export [filename]            Export all tasks to JSON file

EXAMPLES:
    # Add a task with tags and due date
    python task_manager.py add "Finish project" "Complete all tasks" high --tags "work,urgent" --project "CSC299" --due tomorrow
    
    # List overdue tasks
    python task_manager.py list --overdue
    
    # List tasks due today
    python task_manager.py list --due-today
    
    # Search in tags only
    python task_manager.py search "urgent" --in tags
    
    # Update task with multiple fields
    python task_manager.py update 1 --status in_progress --priority high --due +7d
    
    # Bulk update multiple tasks
    python task_manager.py bulk-update "1,2,3" completed
    
    # List all projects
    python task_manager.py projects

STATUS VALUES: pending, in_progress, completed
PRIORITY VALUES: low, medium, high
"""
    print(help_text)


def parse_args(args: List[str]) -> Dict[str, Any]:
    """Parse command-line arguments including flags."""
    parsed = {"positional": [], "flags": {}}
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                parsed["flags"][key] = args[i + 1]
                i += 2
            else:
                parsed["flags"][key] = True
                i += 1
        else:
            parsed["positional"].append(args[i])
            i += 1
    return parsed


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Error: No command specified.")
        print("Use 'python task_manager.py help' for usage information.")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    task_manager = TaskManager()
    parsed = parse_args(sys.argv[2:])
    
    if command == "help":
        print_help()
    
    elif command == "add":
        if len(parsed["positional"]) < 1:
            print("Error: Task title is required.")
            print("Usage: python task_manager.py add <title> [description] [priority] [--tags tag1,tag2] [--project PROJECT] [--due DATE]")
            sys.exit(1)
        
        title = parsed["positional"][0]
        description = parsed["positional"][1] if len(parsed["positional"]) > 1 else ""
        priority = parsed["positional"][2] if len(parsed["positional"]) > 2 else parsed["flags"].get("priority", "medium")
        
        tags = None
        if parsed["flags"].get("tags"):
            tags = [t.strip() for t in parsed["flags"]["tags"].split(",")]
        
        project = parsed["flags"].get("project")
        due_date = parsed["flags"].get("due")
        
        task_manager.add_task(title, description, priority, tags, project, due_date)
    
    elif command == "list":
        status_filter = parsed["positional"][0] if len(parsed["positional"]) > 0 else parsed["flags"].get("status")
        priority_filter = parsed["positional"][1] if len(parsed["positional"]) > 1 else parsed["flags"].get("priority")
        
        task_manager.list_tasks(
            status_filter=status_filter,
            priority_filter=priority_filter,
            tag_filter=parsed["flags"].get("tag"),
            project_filter=parsed["flags"].get("project"),
            overdue_only=parsed["flags"].get("overdue", False),
            due_today=parsed["flags"].get("due-today", False),
            due_this_week=parsed["flags"].get("due-week", False)
        )
    
    elif command == "search":
        if len(parsed["positional"]) < 1:
            print("Error: Search query is required.")
            print("Usage: python task_manager.py search <query> [--in title|description|tags|project|all]")
            sys.exit(1)
        
        query = " ".join(parsed["positional"])
        search_in = parsed["flags"].get("in", "all")
        task_manager.search_tasks(query, search_in)
    
    elif command == "update":
        if len(parsed["positional"]) < 1:
            print("Error: Task ID is required.")
            print("Usage: python task_manager.py update <id> [--title TITLE] [--desc DESCRIPTION] [--priority PRIORITY] [--status STATUS] [--tags tag1,tag2] [--project PROJECT] [--due DATE]")
            sys.exit(1)
        
        try:
            task_id = int(parsed["positional"][0])
            
            tags = None
            if parsed["flags"].get("tags"):
                tags = [t.strip() for t in parsed["flags"]["tags"].split(",")]
            
            task_manager.update_task(
                task_id=task_id,
                title=parsed["flags"].get("title"),
                description=parsed["flags"].get("desc"),
                priority=parsed["flags"].get("priority"),
                status=parsed["flags"].get("status"),
                tags=tags,
                project=parsed["flags"].get("project"),
                due_date=parsed["flags"].get("due")
            )
        except ValueError:
            print("Error: Task ID must be a number.")
            sys.exit(1)
    
    elif command == "add-tags":
        if len(parsed["positional"]) < 2:
            print("Error: Task ID and at least one tag required.")
            sys.exit(1)
        
        try:
            task_id = int(parsed["positional"][0])
            tags = parsed["positional"][1:]
            task_manager.add_tags(task_id, tags)
        except ValueError:
            print("Error: Task ID must be a number.")
            sys.exit(1)
    
    elif command == "remove-tags":
        if len(parsed["positional"]) < 2:
            print("Error: Task ID and at least one tag required.")
            sys.exit(1)
        
        try:
            task_id = int(parsed["positional"][0])
            tags = parsed["positional"][1:]
            task_manager.remove_tags(task_id, tags)
        except ValueError:
            print("Error: Task ID must be a number.")
            sys.exit(1)
    
    elif command == "delete":
        if len(parsed["positional"]) < 1:
            print("Error: Task ID is required.")
            print("Usage: python task_manager.py delete <id>")
            sys.exit(1)
        
        try:
            task_id = int(parsed["positional"][0])
            task_manager.delete_task(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
            sys.exit(1)
    
    elif command == "bulk-update":
        if len(parsed["positional"]) < 2:
            print("Error: Task IDs and status required.")
            print("Usage: python task_manager.py bulk-update <id1,id2,...> <status>")
            sys.exit(1)
        
        try:
            task_ids = [int(id.strip()) for id in parsed["positional"][0].split(",")]
            new_status = parsed["positional"][1]
            task_manager.bulk_update_status(task_ids, new_status)
        except ValueError:
            print("Error: Task IDs must be numbers.")
            sys.exit(1)
    
    elif command == "bulk-delete":
        if len(parsed["positional"]) < 1:
            print("Error: Task IDs required.")
            print("Usage: python task_manager.py bulk-delete <id1,id2,...>")
            sys.exit(1)
        
        try:
            task_ids = [int(id.strip()) for id in parsed["positional"][0].split(",")]
            task_manager.bulk_delete(task_ids)
        except ValueError:
            print("Error: Task IDs must be numbers.")
            sys.exit(1)
    
    elif command == "stats":
        task_manager.get_statistics()
    
    elif command == "projects":
        task_manager.list_projects()
    
    elif command == "tags":
        task_manager.list_tags()
    
    elif command == "export":
        filename = parsed["positional"][0] if parsed["positional"] else None
        task_manager.export_tasks(filename)
    
    else:
        print(f"Error: Unknown command '{command}'.")
        print("Use 'python task_manager.py help' for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()

