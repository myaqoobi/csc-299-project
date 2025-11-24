from .task_manager import TaskManager

def inc(n: int) -> int:
    return n + 1


def main() -> None:
    """Main entry point for tasks3 - Enhanced Task Manager."""
    print("=" * 60)
    print("Enhanced Task Manager - Tasks3")
    print("=" * 60)
    print("\nThis is the enhanced task manager with Notion-inspired features.")
    print("Use the TaskManager class to manage your tasks.")
    print("\nExample usage:")
    print("  from tasks3 import TaskManager")
    print("  tm = TaskManager()")
    print("  tm.add_task('Complete project', priority='high')")
    print("  tm.list_tasks()")
    print("  tm.get_statistics()")
    print()
    
    # Demonstrate functionality
    tm = TaskManager(data_file="demo_tasks.json")
    print("Demo: Adding sample tasks...")
    tm.add_task("Learn Python", "Study Python basics", "high", tags=["study", "coding"])
    tm.add_task("Complete homework", "Finish CSC299 assignment", "medium", project="CSC299")
    tm.add_task("Buy groceries", "Milk, eggs, bread", "low", due_date="tomorrow")
    print("\nDemo: Listing all tasks...")
    tm.list_tasks()
    print("\nDemo: Statistics...")
    tm.get_statistics()
    print("\n" + "=" * 60)
