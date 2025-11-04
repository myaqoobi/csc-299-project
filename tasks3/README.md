# Task 3 - Task Manager with Testing

**What is this?**  
Same enhanced task manager as Task 2, but now packaged with `uv` and includes pytest tests.

**Key differences from Task 2:**
- ✅ Uses `uv` for package management
- ✅ Has pytest test suite (6 tests)
- ✅ Can be run as a package: `uv run tasks3`
- ✅ Includes the required `inc()` function test

**How to run it:**
```bash
# Run the demo
uv run tasks3

# Run tests
uv run pytest
```

**What's tested:**
- Basic task operations (add, update, delete)
- Tags and projects
- Task filtering

**Requirements:** `uv` (installed) and pytest (auto-installed via uv)

This is the same TaskManager as tasks2, just packaged and tested properly! 🎯
