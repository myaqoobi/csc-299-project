#!/usr/bin/env python3
"""
Test suite for TaskManager using pytest
"""

import pytest
import os
import json
import tempfile
from datetime import datetime, timedelta
from task_manager import TaskManager


class TestTaskManager:
    """Test cases for TaskManager class."""
    
    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        fd, path = tempfile.mkstemp(suffix='.json')
        yield path
        os.close(fd)
        if os.path.exists(path):
            os.remove(path)
    
    @pytest.fixture
    def task_manager(self, temp_file):
        """Create a TaskManager instance with a temporary file."""
        return TaskManager(data_file=temp_file)
    
    def test_add_task_basic(self, task_manager):
        """Test adding a basic task."""
        result = task_manager.add_task("Test Task", "Test Description", "high")
        assert result is True
        assert len(task_manager.tasks) == 1
        assert task_manager.tasks[0]["title"] == "Test Task"
        assert task_manager.tasks[0]["description"] == "Test Description"
        assert task_manager.tasks[0]["priority"] == "high"
        assert task_manager.tasks[0]["status"] == "pending"
    
    def test_add_task_with_tags(self, task_manager):
        """Test adding a task with tags."""
        result = task_manager.add_task(
            "Tagged Task", 
            description="", 
            priority="medium",
            tags=["work", "urgent"]
        )
        assert result is True
        assert len(task_manager.tasks) == 1
        assert "work" in task_manager.tasks[0]["tags"]
        assert "urgent" in task_manager.tasks[0]["tags"]
    
    def test_add_task_with_project(self, task_manager):
        """Test adding a task with project."""
        result = task_manager.add_task(
            "Project Task",
            project="CSC299"
        )
        assert result is True
        assert task_manager.tasks[0]["project"] == "CSC299"
    
    def test_add_task_with_due_date(self, task_manager):
        """Test adding a task with due date."""
        result = task_manager.add_task(
            "Due Task",
            due_date="2025-12-31"
        )
        assert result is True
        assert task_manager.tasks[0]["due_date"] == "2025-12-31"
    
    def test_add_task_relative_due_date(self, task_manager):
        """Test adding task with relative due date."""
        result = task_manager.add_task(
            "Tomorrow Task",
            due_date="tomorrow"
        )
        assert result is True
        assert task_manager.tasks[0]["due_date"] is not None
        
        # Verify it's tomorrow's date
        tomorrow = (datetime.now().date() + timedelta(days=1)).isoformat()
        assert task_manager.tasks[0]["due_date"] == tomorrow
    
    def test_add_task_empty_title(self, task_manager):
        """Test that empty title is rejected."""
        result = task_manager.add_task("")
        assert result is False
        assert len(task_manager.tasks) == 0
    
    def test_add_task_invalid_priority(self, task_manager):
        """Test that invalid priority is rejected."""
        result = task_manager.add_task("Test", priority="invalid")
        assert result is False
    
    def test_list_tasks_empty(self, task_manager):
        """Test listing tasks when none exist."""
        # Should not raise exception
        task_manager.list_tasks()
    
    def test_list_tasks_with_filters(self, task_manager):
        """Test listing tasks with filters."""
        task_manager.add_task("Task 1", priority="high", status="pending")
        task_manager.add_task("Task 2", priority="low", status="completed")
        
        # Filter by priority
        task_manager.list_tasks(priority_filter="high")
        
        # Filter by status
        task_manager.list_tasks(status_filter="completed")
    
    def test_search_tasks(self, task_manager):
        """Test searching tasks."""
        task_manager.add_task("Buy groceries", "Get milk and bread")
        task_manager.add_task("Study Python", "Complete chapter 5")
        
        # Search should find matching tasks
        task_manager.search_tasks("groceries")
        task_manager.search_tasks("Python")
    
    def test_update_task_status(self, task_manager):
        """Test updating task status."""
        task_manager.add_task("Test Task")
        task_id = task_manager.tasks[0]["id"]
        
        result = task_manager.update_task(task_id, status="completed")
        assert result is True
        assert task_manager.tasks[0]["status"] == "completed"
        assert task_manager.tasks[0]["completed_at"] is not None
    
    def test_update_task_multiple_fields(self, task_manager):
        """Test updating multiple task fields."""
        task_manager.add_task("Original Title", priority="low")
        task_id = task_manager.tasks[0]["id"]
        
        result = task_manager.update_task(
            task_id,
            title="Updated Title",
            description="Updated Description",
            priority="high"
        )
        assert result is True
        assert task_manager.tasks[0]["title"] == "Updated Title"
        assert task_manager.tasks[0]["description"] == "Updated Description"
        assert task_manager.tasks[0]["priority"] == "high"
    
    def test_add_tags(self, task_manager):
        """Test adding tags to a task."""
        task_manager.add_task("Test Task")
        task_id = task_manager.tasks[0]["id"]
        
        result = task_manager.add_tags(task_id, ["tag1", "tag2"])
        assert result is True
        assert "tag1" in task_manager.tasks[0]["tags"]
        assert "tag2" in task_manager.tasks[0]["tags"]
    
    def test_remove_tags(self, task_manager):
        """Test removing tags from a task."""
        task_manager.add_task("Test Task", tags=["tag1", "tag2", "tag3"])
        task_id = task_manager.tasks[0]["id"]
        
        result = task_manager.remove_tags(task_id, ["tag2"])
        assert result is True
        assert "tag2" not in task_manager.tasks[0]["tags"]
        assert "tag1" in task_manager.tasks[0]["tags"]
        assert "tag3" in task_manager.tasks[0]["tags"]
    
    def test_delete_task(self, task_manager):
        """Test deleting a task."""
        task_manager.add_task("Task to Delete")
        task_id = task_manager.tasks[0]["id"]
        
        result = task_manager.delete_task(task_id)
        assert result is True
        assert len(task_manager.tasks) == 0
    
    def test_delete_nonexistent_task(self, task_manager):
        """Test deleting a task that doesn't exist."""
        result = task_manager.delete_task(999)
        assert result is False
    
    def test_bulk_update_status(self, task_manager):
        """Test bulk updating task status."""
        task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")
        task_manager.add_task("Task 3")
        
        task_ids = [task["id"] for task in task_manager.tasks]
        updated_count = task_manager.bulk_update_status(task_ids, "completed")
        
        assert updated_count == 3
        for task in task_manager.tasks:
            assert task["status"] == "completed"
    
    def test_bulk_delete(self, task_manager):
        """Test bulk deleting tasks."""
        task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")
        task_manager.add_task("Task 3")
        
        task_ids = [task_manager.tasks[0]["id"], task_manager.tasks[1]["id"]]
        deleted_count = task_manager.bulk_delete(task_ids)
        
        assert deleted_count == 2
        assert len(task_manager.tasks) == 1
    
    def test_get_statistics(self, task_manager):
        """Test getting statistics."""
        task_manager.add_task("Task 1", priority="high")
        task_manager.add_task("Task 2", priority="low", status="completed")
        
        # Should not raise exception
        task_manager.get_statistics()
    
    def test_list_projects(self, task_manager):
        """Test listing projects."""
        task_manager.add_task("Task 1", project="Project A")
        task_manager.add_task("Task 2", project="Project B")
        
        # Should not raise exception
        task_manager.list_projects()
    
    def test_list_tags(self, task_manager):
        """Test listing tags."""
        task_manager.add_task("Task 1", tags=["work", "urgent"])
        task_manager.add_task("Task 2", tags=["personal", "work"])
        
        # Should not raise exception
        task_manager.list_tags()
    
    def test_export_tasks(self, task_manager):
        """Test exporting tasks to JSON."""
        task_manager.add_task("Export Task")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            export_file = f.name
        
        try:
            result = task_manager.export_tasks(export_file)
            assert result is True
            assert os.path.exists(export_file)
            
            # Verify exported content
            with open(export_file, 'r') as f:
                exported_data = json.load(f)
                assert len(exported_data) == 1
                assert exported_data[0]["title"] == "Export Task"
        finally:
            if os.path.exists(export_file):
                os.remove(export_file)
    
    def test_parse_due_date_today(self, task_manager):
        """Test parsing 'today' date."""
        date_str = task_manager._parse_due_date("today")
        assert date_str == datetime.now().date().isoformat()
    
    def test_parse_due_date_tomorrow(self, task_manager):
        """Test parsing 'tomorrow' date."""
        date_str = task_manager._parse_due_date("tomorrow")
        tomorrow = (datetime.now().date() + timedelta(days=1)).isoformat()
        assert date_str == tomorrow
    
    def test_parse_due_date_relative(self, task_manager):
        """Test parsing relative date like '+3d'."""
        date_str = task_manager._parse_due_date("+3d")
        expected = (datetime.now().date() + timedelta(days=3)).isoformat()
        assert date_str == expected
    
    def test_parse_due_date_iso(self, task_manager):
        """Test parsing ISO date format."""
        date_str = task_manager._parse_due_date("2025-12-31")
        assert date_str == "2025-12-31"
    
    def test_validate_date(self, task_manager):
        """Test date validation."""
        assert task_manager._validate_date("2025-12-31") is True
        assert task_manager._validate_date("invalid-date") is False
        assert task_manager._validate_date("2025-13-45") is False
    
    def test_get_next_id(self, task_manager):
        """Test getting next ID."""
        assert task_manager._get_next_id() == 1
        
        task_manager.add_task("Task 1")
        assert task_manager._get_next_id() == 2
        
        task_manager.add_task("Task 2")
        assert task_manager._get_next_id() == 3
    
    def test_list_overdue_tasks(self, task_manager):
        """Test listing overdue tasks."""
        past_date = (datetime.now().date() - timedelta(days=1)).isoformat()
        task_manager.add_task("Overdue Task", due_date=past_date)
        task_manager.add_task("Future Task", due_date="2025-12-31")
        
        task_manager.list_tasks(overdue_only=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

