#!/usr/bin/env python3
"""
Interactive chat-style interface for the Enhanced Task Manager (tasks2).

This provides a terminal UI that:
  - Prompts for a command
  - Executes it using the existing TaskManager logic
  - Shows the results
  - Repeats until the user types 'exit' or 'quit'

It reuses the same commands and flags as `task_manager.py`, but instead of
running one command per process, you can stay in this shell and issue many.
"""

import shlex
from typing import List

from task_manager import TaskManager, parse_args, print_help


BASIC_HELP = """
Chat Task Manager (interactive mode)
Type commands similar to the CLI usage in task_manager.py.

Examples:
  add "Finish project" "Complete all tasks" high --tags "school,urgent" --project "CSC299" --due tomorrow
  list --overdue
  search "urgent" --in tags
  update 1 --status completed --priority high
  stats
  projects
  tags

Special commands:
  help         Show full help from task_manager.py
  quit/exit    Leave the chat
"""


def execute_command(tokens: List[str], tm: TaskManager) -> None:
    """
    Execute a single command line (already tokenized) against the TaskManager.

    This mirrors the dispatch logic in task_manager.main(), but without
    using sys.argv or exiting the process, so it can be used in a REPL.
    """
    if not tokens:
        return

    command = tokens[0].lower()

    # Special meta-commands
    if command in {"quit", "exit"}:
        # The caller handles actually exiting the loop.
        print("Goodbye! 👋")
        return

    if command == "help":
        print_help()
        return

    parsed = parse_args(tokens[1:])

    # The following logic is adapted from task_manager.main()
    if command == "add":
        if len(parsed["positional"]) < 1:
            print("Error: Task title is required.")
            print(
                "Usage: add <title> [description] [priority] "
                "[--tags tag1,tag2] [--project PROJECT] [--due DATE]"
            )
            return

        title = parsed["positional"][0]
        description = parsed["positional"][1] if len(parsed["positional"]) > 1 else ""
        priority = (
            parsed["positional"][2]
            if len(parsed["positional"]) > 2
            else parsed["flags"].get("priority", "medium")
        )

        tags = None
        if parsed["flags"].get("tags"):
            tags = [t.strip() for t in parsed["flags"]["tags"].split(",")]

        project = parsed["flags"].get("project")
        due_date = parsed["flags"].get("due")

        tm.add_task(title, description, priority, tags, project, due_date)

    elif command == "list":
        status_filter = (
            parsed["positional"][0]
            if len(parsed["positional"]) > 0
            else parsed["flags"].get("status")
        )
        priority_filter = (
            parsed["positional"][1]
            if len(parsed["positional"]) > 1
            else parsed["flags"].get("priority")
        )

        tm.list_tasks(
            status_filter=status_filter,
            priority_filter=priority_filter,
            tag_filter=parsed["flags"].get("tag"),
            project_filter=parsed["flags"].get("project"),
            overdue_only=parsed["flags"].get("overdue", False),
            due_today=parsed["flags"].get("due-today", False),
            due_this_week=parsed["flags"].get("due-week", False),
        )

    elif command == "search":
        if len(parsed["positional"]) < 1:
            print("Error: Search query is required.")
            print(
                "Usage: search <query> [--in title|description|tags|project|all]"
            )
            return

        query = " ".join(parsed["positional"])
        search_in = parsed["flags"].get("in", "all")
        tm.search_tasks(query, search_in)

    elif command == "update":
        if len(parsed["positional"]) < 1:
            print("Error: Task ID is required.")
            print(
                "Usage: update <id> [--title TITLE] [--desc DESCRIPTION] "
                "[--priority PRIORITY] [--status STATUS] "
                "[--tags tag1,tag2] [--project PROJECT] [--due DATE]"
            )
            return

        try:
            task_id = int(parsed["positional"][0])
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        tags = None
        if parsed["flags"].get("tags"):
            tags = [t.strip() for t in parsed["flags"]["tags"].split(",")]

        tm.update_task(
            task_id=task_id,
            title=parsed["flags"].get("title"),
            description=parsed["flags"].get("desc"),
            priority=parsed["flags"].get("priority"),
            status=parsed["flags"].get("status"),
            tags=tags,
            project=parsed["flags"].get("project"),
            due_date=parsed["flags"].get("due"),
        )

    elif command == "add-tags":
        if len(parsed["positional"]) < 2:
            print("Error: Task ID and at least one tag required.")
            return

        try:
            task_id = int(parsed["positional"][0])
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        tags = parsed["positional"][1:]
        tm.add_tags(task_id, tags)

    elif command == "remove-tags":
        if len(parsed["positional"]) < 2:
            print("Error: Task ID and at least one tag required.")
            return

        try:
            task_id = int(parsed["positional"][0])
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        tags = parsed["positional"][1:]
        tm.remove_tags(task_id, tags)

    elif command == "delete":
        if len(parsed["positional"]) < 1:
            print("Error: Task ID is required.")
            print("Usage: delete <id>")
            return

        try:
            task_id = int(parsed["positional"][0])
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        tm.delete_task(task_id)

    elif command == "bulk-update":
        if len(parsed["positional"]) < 2:
            print("Error: Task IDs and status required.")
            print("Usage: bulk-update <id1,id2,...> <status>")
            return

        try:
            task_ids = [
                int(id_.strip()) for id_ in parsed["positional"][0].split(",")
            ]
        except ValueError:
            print("Error: Task IDs must be numbers.")
            return

        new_status = parsed["positional"][1]
        tm.bulk_update_status(task_ids, new_status)

    elif command == "bulk-delete":
        if len(parsed["positional"]) < 1:
            print("Error: Task IDs required.")
            print("Usage: bulk-delete <id1,id2,...>")
            return

        try:
            task_ids = [
                int(id_.strip()) for id_ in parsed["positional"][0].split(",")
            ]
        except ValueError:
            print("Error: Task IDs must be numbers.")
            return

        tm.bulk_delete(task_ids)

    elif command == "stats":
        tm.get_statistics()

    elif command == "projects":
        tm.list_projects()

    elif command == "tags":
        tm.list_tags()

    elif command == "export":
        filename = parsed["positional"][0] if parsed["positional"] else None
        tm.export_tasks(filename)

    else:
        print(f"Error: Unknown command '{command}'. Type 'help' for options.")


def main() -> None:
    """Run the interactive chat-style shell."""
    tm = TaskManager()

    print("=" * 70)
    print("📋 Enhanced Task Manager – Chat Mode (tasks2)")
    print("=" * 70)
    print(BASIC_HELP)

    while True:
        try:
            line = input("tm> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! 👋")
            break

        if not line:
            continue

        if line.lower() in {"quit", "exit"}:
            print("Goodbye! 👋")
            break

        # Tokenize the line similar to a shell, so quotes work.
        try:
            tokens = shlex.split(line)
        except ValueError as e:
            print(f"Error parsing command: {e}")
            continue

        execute_command(tokens, tm)


if __name__ == "__main__":
    main()


