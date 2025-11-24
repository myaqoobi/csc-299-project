"""
Test suite for TaskManager using pytest
"""

import pytest
import os
import tempfile
from tasks3.task_manager import TaskManager


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
    
    def test_add_task_with_tags_and_project(self, task_manager):
        """Test adding a task with tags and project."""
        result = task_manager.add_task(
            "Tagged Task", 
            description="Task with tags", 
            priority="medium",
            tags=["work", "urgent"],
            project="CSC299"
        )
        assert result is True
        assert len(task_manager.tasks) == 1
        task = task_manager.tasks[0]
        assert task["title"] == "Tagged Task"
        assert "work" in task["tags"]
        assert "urgent" in task["tags"]
        assert task["project"] == "CSC299"
    
    def test_update_task_status(self, task_manager):
        """Test updating a task's status."""
        # Add a task first
        task_manager.add_task("Task to update", priority="low")
        task_id = task_manager.tasks[0]["id"]
        
        # Update status to completed
        result = task_manager.update_task(task_id, status="completed")
        assert result is True
        assert task_manager.tasks[0]["status"] == "completed"
        assert task_manager.tasks[0]["completed_at"] is not None
    
    def test_delete_task(self, task_manager):
        """Test deleting a task."""
        # Add multiple tasks
        task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")
        task_manager.add_task("Task 3")
        
        initial_count = len(task_manager.tasks)
        task_id = task_manager.tasks[1]["id"]  # Delete middle task
        
        result = task_manager.delete_task(task_id)
        assert result is True
        assert len(task_manager.tasks) == initial_count - 1
        assert all(task["id"] != task_id for task in task_manager.tasks)
    
    def test_list_tasks_with_filters(self, task_manager):
        """Test listing tasks with status filter."""
        # Add tasks with different statuses
        task_manager.add_task("Pending Task", priority="high")
        task_manager.add_task("Another Task", priority="medium")
        
        # Update one to completed
        task_id = task_manager.tasks[0]["id"]
        task_manager.update_task(task_id, status="completed")
        
        # Filter by completed status
        completed_tasks = [t for t in task_manager.tasks if t["status"] == "completed"]
        assert len(completed_tasks) == 1
        assert completed_tasks[0]["title"] == "Pending Task"

