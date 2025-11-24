# Quick Start: Task Manager Application

**Feature**: 001-task-manager  
**Last Updated**: 2025-11-18

## Getting Started

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, or Edge from last 2 years)
- Text editor (VS Code, Sublime, or any code editor)
- (Optional) Local web server for development

### No Installation Required!

This is a client-side web application - no npm, no build tools, no dependencies to install. Just open the HTML file in your browser!

## Quick Start (30 seconds)

1. **Download/Clone the files**
2. **Double-click `index.html`** or open it in your browser
3. **Start adding tasks!**

That's it! The app runs entirely in your browser.

## Development Setup

### Option 1: Direct File Opening (Simplest)

```bash
# Just open the file
open index.html  # macOS
start index.html  # Windows
xdg-open index.html  # Linux
```

**Note**: Some features might be limited due to CORS policies when opening local files. Use Option 2 or 3 for full functionality.

### Option 2: Python Simple Server (Recommended)

```bash
# Navigate to project directory
cd path/to/task-manager

# Python 3
python3 -m http.server 8000

# Python 2 (if you're stuck in the past)
python -m SimpleHTTPServer 8000

# Open browser to http://localhost:8000
```

### Option 3: Node.js Serve (If you have Node)

```bash
# Install serve globally (one time)
npm install -g serve

# Run from project directory
serve .

# Open browser to displayed URL (usually http://localhost:3000)
```

### Option 4: VS Code Live Server Extension

1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"
4. Browser opens automatically

## Project Structure

```
task-manager/
├── index.html          # Main HTML structure
├── styles.css          # All styles (CSS Grid, Flexbox)
├── app.js              # Application initialization
├── taskManager.js      # Core task logic (CRUD operations)
├── storage.js          # localStorage abstraction
├── ui.js               # DOM manipulation and rendering
├── utils.js            # Helper functions
└── README.md           # Documentation
```

## File Overview

### index.html
Main application structure - semantic HTML5 with:
- Task form (add/edit)
- Task list container
- Filter controls
- Statistics display
- Modal dialogs

### styles.css
Complete styling with:
- CSS Grid layout for responsive design
- Flexbox for component alignment
- CSS Custom Properties for theming
- Mobile-first responsive design
- Print styles (bonus!)

### app.js
Application coordinator:
- Initialize the app
- Setup event listeners
- Coordinate components
- Handle user interactions

### taskManager.js
Core business logic:
- `createTask(data)` - Add new task
- `updateTask(id, updates)` - Modify task
- `deleteTask(id)` - Remove task
- `completeTask(id)` / `uncompleteTask(id)` - Toggle status
- `getAllTasks()` - Get all tasks
- `filterTasks(criteria)` - Search and filter
- `getStatistics()` - Calculate stats

### storage.js
Data persistence layer:
- `loadTasks()` - Read from localStorage
- `saveTasks(tasks)` - Write to localStorage
- `exportToJSON()` - Generate JSON backup
- `exportToCSV()` - Generate CSV export
- Error handling and recovery

### ui.js
User interface rendering:
- `renderTaskList(tasks)` - Display tasks
- `renderTask(task)` - Single task card
- `renderStatistics(stats)` - Stats display
- `showTaskForm()` / `hideTaskForm()` - Modal management
- `showError()` / `showSuccess()` - User feedback

### utils.js
Shared utilities:
- `generateId()` - Unique task IDs
- `formatDate(date)` - Display formatting
- `isOverdue(date)` - Date comparison
- `sanitizeHTML(str)` - XSS prevention
- `parseTags(input)` - Tag parsing

## Usage Guide

### Adding a Task

1. Type task title in the input field at top
2. (Optional) Click "Add Details" to expand form
3. (Optional) Add description, priority, due date, tags
4. Click "Add Task" or press Enter
5. Task appears in the list immediately

**Quick Add**: Just type title and press Enter!

### Completing a Task

- Click the checkbox next to the task
- Task gets strikethrough and checkmark
- Moves to "Completed" section (if view is grouped)

### Editing a Task

1. Click "Edit" button on task card
2. Modify any fields
3. Click "Save" or press Enter
4. Changes save immediately

### Deleting a Task

1. Click "Delete" button on task card
2. Confirm deletion in dialog
3. Task removed permanently

**Warning**: Deletion cannot be undone! Export data regularly for backup.

### Filtering & Search

**Search**: Type in search box to filter by title, description, or tags

**Filter by Status**:
- All Tasks
- Active Only
- Completed Only

**Filter by Priority**:
- All Priorities
- High Priority
- Medium Priority
- Low Priority

**Quick Filters**:
- Overdue Tasks (past due date)
- Due Today
- Due This Week

### Exporting Data

**JSON Export** (for backup/restore):
1. Click "Export" button
2. Select "JSON"
3. Save file (e.g., `tasks-2025-11-18.json`)

**CSV Export** (for spreadsheets):
1. Click "Export" button
2. Select "CSV"
3. Open in Excel/Google Sheets

## Keyboard Shortcuts

- `Enter` in title field: Add new task (quick mode)
- `Escape` in form: Cancel edit/add
- `Ctrl/Cmd + F`: Focus search (if implemented)

## Data Storage

### Where is my data stored?

All task data is stored in your browser's localStorage:

```
Browser > Developer Tools > Application > Local Storage > [your domain]
Key: "taskManager_tasks"
```

### Storage Capacity

- **Typical Limit**: 5-10 MB per domain
- **Task Size**: ~250 bytes per task
- **Capacity**: Thousands of tasks

### Data Privacy

✅ **Your data never leaves your device**  
✅ **No server, no cloud, no tracking**  
✅ **Complete privacy**  

⚠️ **Your data is NOT synced across devices**  
⚠️ **Clearing browser data will delete tasks**  
⚠️ **Use Export feature regularly for backups**

## Browser Compatibility

✅ **Chrome** 90+ (2021+)  
✅ **Firefox** 88+ (2021+)  
✅ **Safari** 14+ (2020+)  
✅ **Edge** 90+ (2021+)

**Features Used**:
- localStorage API (universal support)
- CSS Grid & Flexbox (excellent support)
- ES6+ JavaScript (needs modern browser)
- `<input type="date">` (good mobile support)

## Mobile Usage

The app is fully responsive:

- **320px+**: Mobile phones (portrait)
- **768px+**: Tablets
- **1024px+**: Desktops

**Touch Optimized**:
- 44px+ tap targets
- Swipe gestures (if implemented)
- Mobile-friendly date picker

## Troubleshooting

### Tasks disappear after browser refresh

**Cause**: localStorage might be disabled or in private/incognito mode  
**Solution**:
- Exit private browsing
- Check browser settings for localStorage
- Use Export feature before closing browser

### "Storage Full" error

**Cause**: localStorage quota exceeded (rare)  
**Solution**:
- Export tasks to JSON
- Delete old completed tasks
- Clear other site data from browser

### Date picker doesn't work

**Cause**: Older browser version  
**Solution**:
- Update browser to latest version
- Or manually type date as YYYY-MM-DD

### Task title has weird characters

**Cause**: Special characters not properly escaped  
**Solution**: This is a bug - avoid using `<`, `>`, `&` in titles until fixed

## Development Tips

### Viewing localStorage

**Chrome DevTools**:
1. F12 to open DevTools
2. Application tab
3. Local Storage > [your domain]
4. See `taskManager_tasks` key

**Edit Manually**:
- Right-click key
- Edit Value
- Must be valid JSON!

### Testing with Dummy Data

Add this to browser console:

```javascript
// Generate 10 random tasks
for (let i = 0; i < 10; i++) {
  taskManager.createTask({
    title: `Test Task ${i + 1}`,
    description: `This is test task number ${i + 1}`,
    priority: ["low", "medium", "high"][i % 3],
    dueDate: new Date(Date.now() + i * 86400000).toISOString().split('T')[0],
    tags: ["test", `category-${i % 3}`]
  });
}
```

### Resetting All Data

```javascript
localStorage.clear();
location.reload();
```

## Next Steps

1. **Use it**: Add your real tasks!
2. **Customize**: Modify CSS colors, fonts, layout
3. **Extend**: Add features (dark mode, recurring tasks, etc.)
4. **Deploy**: Put it on GitHub Pages (see deployment guide)

## Deployment Guide

### GitHub Pages (Free Hosting)

1. Create GitHub repository
2. Push code to repository
3. Go to Settings > Pages
4. Select branch (usually `main`) and root folder
5. Save
6. Access at `https://[username].github.io/[repo-name]`

### Other Options

- **Netlify**: Drag-and-drop deployment
- **Vercel**: Connect GitHub repo
- **Cloudflare Pages**: Fast global CDN
- **Local**: Just open `index.html` anywhere!

## Getting Help

**Check the spec**: `specs/001-task-manager/spec.md`  
**Check the plan**: `specs/001-task-manager/plan.md`  
**Check the data model**: `specs/001-task-manager/data-model.md`

## License

MIT License - feel free to use, modify, and distribute!

---

**Ready to code?** Open your text editor and start with `index.html`! 🚀

