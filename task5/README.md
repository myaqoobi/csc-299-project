# Task Manager - Built with Spec-Driven Development

A simple, elegant task management application built using **Spec-Driven Development (SDD)** methodology with GitHub's Spec Kit. Created for CSC299 - Task 5 assignment.

## 🎯 What is Spec-Driven Development?

Spec-Driven Development is an AI-native development methodology that emphasizes creating clear specifications before implementation. This project was built using:

1. **`/speckit.constitution`** - Established project principles
2. **`/speckit.specify`** - Defined requirements and user stories  
3. **`/speckit.plan`** - Created technical implementation plan
4. **`/speckit.tasks`** - Generated actionable task breakdown
5. **`/speckit.implement`** - Executed implementation following the plan

All specifications are documented in the `specs/001-task-manager/` directory.

## ✨ Features

- ✅ **Quick Task Entry** - Add tasks with just a title, or expand for details
- ✅ **Task Management** - Create, edit, delete, and complete tasks
- ✅ **Organization** - Priorities (high/medium/low), due dates, and tags
- ✅ **Filtering & Search** - Find tasks by status, priority, overdue, or search text
- ✅ **Statistics Dashboard** - View counts of total, active, and completed tasks
- ✅ **Data Export** - Export tasks to JSON (backup) or CSV (spreadsheet)
- ✅ **Local Storage** - All data persists in your browser, no backend required
- ✅ **Responsive Design** - Works on mobile, tablet, and desktop
- ✅ **Clean UI** - Modern, intuitive interface built with vanilla HTML/CSS/JS

## 🚀 Quick Start

### Option 1: Open Directly

1. Download all files to a directory
2. Double-click `index.html` to open in your browser
3. Start managing tasks!

### Option 2: Local Server (Recommended)

```bash
# Using Python 3
python3 -m http.server 8000

# Then open http://localhost:8000 in your browser
```

### Option 3: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click `index.html` → "Open with Live Server"

## 📁 Project Structure

```
task-manager/
├── index.html           # Main HTML structure
├── styles.css           # Complete styling (CSS Grid, responsive)
├── app.js               # Application initialization & coordination
├── taskManager.js       # Core task logic (CRUD operations)
├── storage.js           # localStorage abstraction
├── ui.js                # DOM manipulation & rendering
├── utils.js             # Helper functions
├── README.md            # This file
└── specs/               # Spec-Driven Development documentation
    └── 001-task-manager/
        ├── spec.md          # Feature specification
        ├── plan.md          # Technical implementation plan
        ├── data-model.md    # Data structure definitions
        ├── quickstart.md    # Development guide
        └── tasks.md         # Task breakdown
```

## 💡 Usage

### Adding a Task

1. Type task title in the input field
2. Press Enter or click "Add Task"
3. (Optional) Click "+ Add Details" for description, priority, due date, and tags

### Managing Tasks

- **Complete**: Click the checkbox next to a task
- **Edit**: Click the "Edit" button on a task card
- **Delete**: Click the "Delete" button (with confirmation)

### Filtering Tasks

- **Search**: Type to search in titles, descriptions, and tags
- **Status**: Filter by All/Active/Completed
- **Priority**: Filter by All/High/Medium/Low
- **Overdue**: Check to see only overdue tasks

### Exporting Data

1. Click "📥 Export" button
2. Choose format (JSON for backup, CSV for spreadsheet)
3. File downloads automatically

## 🎨 Technical Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Storage**: Browser localStorage API
- **No Dependencies**: Zero frameworks, libraries, or build tools
- **No Backend**: Runs entirely client-side

## 🏗️ Architecture

### Separation of Concerns

- **app.js**: Application coordination and event handling
- **taskManager.js**: Business logic (data validation, CRUD operations)
- **storage.js**: Data persistence layer (localStorage abstraction)
- **ui.js**: Presentation layer (DOM rendering and manipulation)
- **utils.js**: Shared utilities (formatting, validation, sanitization)

### Data Flow

```
User Action → App.js → TaskManager.js → Storage.js → localStorage
                                      ↓
                                   UI.js → DOM Update
```

## 📊 Data Model

### Task Structure

```javascript
{
  id: "task_1700000000000_abc123",
  title: "Complete homework",
  description: "Build task manager with spec-kit",
  status: "incomplete" | "complete",
  priority: "high" | "medium" | "low",
  dueDate: "2025-11-19" | null,
  tags: ["school", "urgent"],
  createdAt: "2025-11-18T10:30:00.000Z",
  completedAt: "2025-11-18T14:20:00.000Z" | null
}
```

See `specs/001-task-manager/data-model.md` for complete data model documentation.

## 🧪 Testing

### Manual Testing Checklist

- [ ] Create task with just title
- [ ] Create task with all details
- [ ] Edit task and verify changes persist
- [ ] Delete task with confirmation
- [ ] Mark task complete/incomplete
- [ ] Search for tasks
- [ ] Filter by status, priority, overdue
- [ ] Export to JSON and CSV
- [ ] Refresh browser and verify data persists
- [ ] Test on mobile device

### Browser Testing

Tested on:
- ✅ Chrome 120+
- ✅ Firefox 121+
- ✅ Safari 17+
- ✅ Edge 120+

## 🔒 Privacy & Security

- **100% Local**: All data stored in your browser only
- **No Tracking**: Zero analytics, no data collection
- **No Backend**: No server communication, fully offline
- **XSS Protection**: User input sanitized before rendering

## 🐛 Known Limitations

- Data stored per browser (not synced across devices)
- localStorage limit: ~5-10MB (sufficient for thousands of tasks)
- Clearing browser data will delete tasks (use Export feature!)
- No undo/redo functionality
- No recurring tasks
- No natural language date parsing

## 📚 Spec-Driven Development Documentation

All specifications created during development are in `specs/001-task-manager/`:

- **Constitution** (`.specify/memory/constitution.md`) - Project principles
- **Specification** (`spec.md`) - Feature requirements and user stories
- **Implementation Plan** (`plan.md`) - Technical architecture and decisions
- **Data Model** (`data-model.md`) - Data structure definitions
- **Tasks** (`tasks.md`) - Implementation task breakdown
- **Quick Start** (`quickstart.md`) - Development guide

## 🎓 Educational Value

This project demonstrates:

- ✅ **Spec-Driven Development methodology** using GitHub Spec Kit
- ✅ **Modern vanilla JavaScript** without framework dependencies
- ✅ **Clean architecture** with separation of concerns
- ✅ **LocalStorage API** for client-side persistence
- ✅ **Responsive CSS** with Grid and Flexbox
- ✅ **Progressive enhancement** principles
- ✅ **User-centric design** with clear UI/UX

## 🤝 Contributing

This is an educational project for CSC299. The development process followed Spec-Driven Development methodology.

## 📄 License

MIT License - Free to use, modify, and distribute.

## 👤 Author

Built for CSC299 - Task 5: Spec-Driven Development Assignment

---

## 🚀 Future Enhancements (Out of Current Scope)

- Dark mode toggle
- Drag-and-drop task reordering
- Recurring tasks
- Natural language date parsing ("tomorrow", "next week")
- Calendar view
- Data sync across devices
- PWA (Progressive Web App) capabilities
- Mobile app versions

---

**Happy Task Managing! 📋✨**

For questions or issues, refer to the specification documents in `specs/001-task-manager/`.

