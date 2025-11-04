#!/usr/bin/env python3
"""
Enhanced Task Management Application
CSC299 Project - Task Manager with Notion-inspired Features
"""

import json
import os
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
        """Add a new task to the list with enhanced features."""
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
        """Print a single task in a formatted way."""
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
        print("-" * 40)
    
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
    
    def get_statistics(self) -> None:
        """Display task statistics."""
        if not self.tasks:
            print("No tasks found.")
            return
        
        total_tasks = len(self.tasks)
        pending = len([t for t in self.tasks if t.get("status") == "pending"])
        in_progress = len([t for t in self.tasks if t.get("status") == "in_progress"])
        completed = len([t for t in self.tasks if t.get("status") == "completed"])
        
        print(f"\n{'='*60}")
        print("📊 TASK STATISTICS")
        print(f"{'='*60}")
        print(f"Total Tasks: {total_tasks}")
        print(f"⏳ Pending: {pending}")
        print(f"🔄 In Progress: {in_progress}")
        print(f"✅ Completed: {completed}")
        
        if total_tasks > 0:
            completion_rate = (completed / total_tasks) * 100
            print(f"📈 Completion Rate: {completion_rate:.1f}%")

