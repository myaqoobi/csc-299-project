# CSC299 Project – Personal Task Management (Ordered Overview)

This repository contains your complete project, organized in the order your professor expects:

1) Task 1 – Prototype CLI Task Manager
2) Task 2 – Enhanced CLI Task Manager (Notion-inspired, with tests)
3) Class Project Web App (Next.js Todo UI)

---

## 1) Task 1 – Prototype (CLI)

- Folder: `tasks1/`
- Files: `task_manager.py`, `README.md`
- Storage: `tasks.json` (auto-created when running)

Quick start:
```bash
cd tasks1
python3 task_manager.py help
python3 task_manager.py add "Buy groceries" "Get milk and bread" high
python3 task_manager.py list
```

---

## 2) Task 2 – Enhanced (CLI, Notion-inspired, with tests)

- Folder: `tasks2/`
- Files: `task_manager.py`, `test_task_manager.py`, `README.md`
- Features: tags, projects, due dates (incl. relative formats), advanced filters, bulk ops, rich stats, export, pytest tests

Quick start:
```bash
cd tasks2
python3 task_manager.py help
python3 task_manager.py add "Finish project" "Complete all tasks" high --tags "work,urgent" --project "CSC299" --due tomorrow
python3 task_manager.py list --overdue
pytest test_task_manager.py -v
```

Common commands:
```bash
# Search
python3 task_manager.py search "urgent" --in tags

# Update
python3 task_manager.py update 1 --status in_progress --priority high --due +3d

# Bulk
python3 task_manager.py bulk-update "1,2" completed
python3 task_manager.py bulk-delete "1,2"

# Stats / Organization
python3 task_manager.py stats
python3 task_manager.py projects
python3 task_manager.py tags
```

---

## 3) Class Project Web App (Next.js Todo UI)

- Folders: `app/`, `components/`, `public/`
- Start locally:
```bash
npm install
npm run dev
# Open http://localhost:3000
```

---

## Repository Tree (key parts)

```
.
├── tasks1/
│   ├── README.md
│   └── task_manager.py
├── tasks2/
│   ├── README.md
│   ├── task_manager.py
│   └── test_task_manager.py
├── app/                     # Next.js app
├── components/
├── public/
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md (this file)
```

---

## Notes
- Tasks 1 and 2 are Python CLI apps and portable across Windows/macOS/Linux.
- State is stored in JSON (`tasks.json`) for CLI apps, created automatically.
- The web app is a separate UI (localStorage-based) and not required for the CLI deliverables.

For detailed feature lists and examples, see:
- `tasks1/README.md`
- `tasks2/README.md`

