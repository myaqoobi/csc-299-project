# Data Model: Task Manager Application

**Feature**: 001-task-manager  
**Last Updated**: 2025-11-18

## Task Entity

### Structure

```javascript
{
  id: string,              // Unique identifier: "task_{timestamp}_{random}"
  title: string,           // Required: 1-500 characters
  description: string,     // Optional: 0-2000 characters
  status: string,          // "incomplete" | "complete"
  priority: string,        // "low" | "medium" | "high"
  dueDate: string | null,  // ISO date string "YYYY-MM-DD" or null
  tags: string[],          // Array of tag strings, default []
  createdAt: string,       // ISO 8601 timestamp
  completedAt: string | null  // ISO 8601 timestamp or null
}
```

### Example Task

```javascript
{
  id: "task_1700000000000_a7b3c9",
  title: "Complete CSC299 homework",
  description: "Use spec-kit to build a task manager application",
  status: "incomplete",
  priority: "high",
  dueDate: "2025-11-19",
  tags: ["school", "programming", "urgent"],
  createdAt: "2025-11-18T10:30:00.000Z",
  completedAt: null
}
```

### Field Specifications

#### id
- **Type**: `string`
- **Format**: `task_{timestamp}_{randomHex}`
- **Generation**: `task_${Date.now()}_${Math.random().toString(16).slice(2,8)}`
- **Purpose**: Unique identifier for task operations
- **Validation**: Must be unique across all tasks

#### title
- **Type**: `string`
- **Required**: Yes
- **Min Length**: 1 character
- **Max Length**: 500 characters
- **Validation**: Cannot be empty or only whitespace
- **Sanitization**: Trim whitespace, escape HTML

#### description
- **Type**: `string`
- **Required**: No
- **Default**: `""` (empty string)
- **Max Length**: 2000 characters
- **Validation**: None (can be empty)
- **Sanitization**: Trim whitespace, escape HTML

#### status
- **Type**: `string` (enum)
- **Required**: Yes
- **Values**: `"incomplete"` | `"complete"`
- **Default**: `"incomplete"`
- **Validation**: Must be one of the allowed values

#### priority
- **Type**: `string` (enum)
- **Required**: Yes
- **Values**: `"low"` | `"medium"` | `"high"`
- **Default**: `"medium"`
- **Validation**: Must be one of the allowed values
- **Display**: 
  - `high`: Red badge, red accent
  - `medium`: Yellow badge, yellow accent
  - `low`: Green badge, green accent

#### dueDate
- **Type**: `string | null`
- **Required**: No
- **Format**: ISO date string `"YYYY-MM-DD"`
- **Default**: `null`
- **Validation**: Must be valid date string or null
- **Display**: Show relative time ("Today", "Tomorrow", "3 days") and highlight if overdue

#### tags
- **Type**: `string[]` (array of strings)
- **Required**: No
- **Default**: `[]` (empty array)
- **Validation**: 
  - Each tag: 1-30 characters
  - Max 10 tags per task
  - Automatically deduplicate
  - Trim whitespace
- **Input Format**: Comma-separated string converted to array
- **Example**: `"work, urgent, client"` → `["work", "urgent", "client"]`

#### createdAt
- **Type**: `string`
- **Required**: Yes
- **Format**: ISO 8601 timestamp `"YYYY-MM-DDTHH:mm:ss.sssZ"`
- **Generation**: `new Date().toISOString()`
- **Purpose**: Track when task was created, enable sorting by creation date

#### completedAt
- **Type**: `string | null`
- **Required**: No
- **Default**: `null`
- **Format**: ISO 8601 timestamp `"YYYY-MM-DDTHH:mm:ss.sssZ"`
- **Updates**: Set when status changes to `"complete"`, cleared when uncompleted
- **Purpose**: Track completion time, calculate time-to-completion

## LocalStorage Schema

### Key-Value Structure

```javascript
// Key
"taskManager_tasks"

// Value (JSON serialized array)
"[{...task1...}, {...task2...}, {...task3...}]"
```

### Full Example

```javascript
localStorage.setItem(
  "taskManager_tasks",
  JSON.stringify([
    {
      id: "task_1700000000000_a7b3c9",
      title: "Complete homework",
      description: "Build task manager with spec-kit",
      status: "incomplete",
      priority: "high",
      dueDate: "2025-11-19",
      tags: ["school", "urgent"],
      createdAt: "2025-11-18T10:30:00.000Z",
      completedAt: null
    },
    {
      id: "task_1700010000000_b8c4d1",
      title: "Buy groceries",
      description: "",
      status: "complete",
      priority: "medium",
      dueDate: "2025-11-18",
      tags: ["personal", "shopping"],
      createdAt: "2025-11-17T15:20:00.000Z",
      completedAt: "2025-11-18T09:45:00.000Z"
    }
  ])
);
```

### Storage Size Estimation

- Average task size: ~250 bytes
- 100 tasks: ~25 KB
- 500 tasks: ~125 KB
- 1000 tasks: ~250 KB

**Capacity**: localStorage typically provides 5-10 MB, sufficient for thousands of tasks.

## Data Operations

### Create Task
```javascript
function createTask(taskData) {
  const task = {
    id: generateId(),
    title: sanitize(taskData.title.trim()),
    description: sanitize(taskData.description?.trim() || ""),
    status: "incomplete",
    priority: taskData.priority || "medium",
    dueDate: taskData.dueDate || null,
    tags: parseTags(taskData.tags),
    createdAt: new Date().toISOString(),
    completedAt: null
  };
  
  // Validate
  if (!task.title) throw new Error("Title is required");
  if (!["low", "medium", "high"].includes(task.priority)) {
    throw new Error("Invalid priority");
  }
  
  return task;
}
```

### Update Task
```javascript
function updateTask(id, updates) {
  const task = getTaskById(id);
  if (!task) throw new Error("Task not found");
  
  // Merge updates
  const updated = {
    ...task,
    ...updates,
    id: task.id, // Prevent ID change
    createdAt: task.createdAt, // Prevent creation date change
  };
  
  // Re-validate
  if (updated.title && !updated.title.trim()) {
    throw new Error("Title cannot be empty");
  }
  
  return updated;
}
```

### Complete Task
```javascript
function completeTask(id) {
  const task = getTaskById(id);
  if (!task) throw new Error("Task not found");
  
  return {
    ...task,
    status: "complete",
    completedAt: new Date().toISOString()
  };
}
```

### Uncomplete Task
```javascript
function uncompleteTask(id) {
  const task = getTaskById(id);
  if (!task) throw new Error("Task not found");
  
  return {
    ...task,
    status: "incomplete",
    completedAt: null
  };
}
```

## Filtering & Search

### Filter Criteria Object
```javascript
{
  status: "incomplete" | "complete" | "all",
  priority: "high" | "medium" | "low" | "all",
  overdue: boolean,
  tag: string | null,
  search: string | null
}
```

### Filter Logic

**Status Filter**:
```javascript
tasks.filter(task => 
  criteria.status === "all" || task.status === criteria.status
)
```

**Priority Filter**:
```javascript
tasks.filter(task => 
  criteria.priority === "all" || task.priority === criteria.priority
)
```

**Overdue Filter**:
```javascript
tasks.filter(task => 
  task.dueDate && new Date(task.dueDate) < new Date()
)
```

**Tag Filter**:
```javascript
tasks.filter(task => 
  task.tags.includes(criteria.tag)
)
```

**Search Filter** (searches title, description, tags):
```javascript
tasks.filter(task => {
  const query = criteria.search.toLowerCase();
  return (
    task.title.toLowerCase().includes(query) ||
    task.description.toLowerCase().includes(query) ||
    task.tags.some(tag => tag.toLowerCase().includes(query))
  );
})
```

## Statistics Model

```javascript
{
  total: number,        // Total number of tasks
  active: number,       // Incomplete tasks
  completed: number,    // Complete tasks
  overdue: number,      // Incomplete tasks past due date
  dueToday: number,     // Tasks due today
  dueSoon: number,      // Tasks due in next 7 days
  highPriority: number, // High priority incomplete tasks
  byTag: {              // Task counts by tag
    [tagName]: number
  }
}
```

## Export Formats

### JSON Export
Full data structure, preserves all fields for backup/restore:

```json
[
  {
    "id": "task_1700000000000_a7b3c9",
    "title": "Complete homework",
    "description": "Build task manager with spec-kit",
    "status": "incomplete",
    "priority": "high",
    "dueDate": "2025-11-19",
    "tags": ["school", "urgent"],
    "createdAt": "2025-11-18T10:30:00.000Z",
    "completedAt": null
  }
]
```

### CSV Export
Simplified format for spreadsheet import:

```csv
Title,Description,Status,Priority,Due Date,Tags,Created,Completed
"Complete homework","Build task manager with spec-kit","incomplete","high","2025-11-19","school,urgent","2025-11-18T10:30:00.000Z",""
"Buy groceries","","complete","medium","2025-11-18","personal,shopping","2025-11-17T15:20:00.000Z","2025-11-18T09:45:00.000Z"
```

## Data Validation Rules

### On Create
- ✅ Title required (1-500 chars)
- ✅ Priority must be valid enum
- ✅ Due date must be valid date or null
- ✅ Tags must be array of strings

### On Update
- ✅ ID cannot change
- ✅ Created date cannot change
- ✅ All create rules apply to updated fields

### On Delete
- ✅ Task must exist
- ✅ Confirmation required from user

## Error Handling

### localStorage Errors
- `QuotaExceededError`: Notify user, suggest export + cleanup
- `SecurityError`: Fall back to in-memory mode, show warning
- Parse errors: Log to console, return empty array, preserve corrupt data

### Validation Errors
- Clear, user-friendly messages
- Indicate which field failed validation
- Provide guidance on valid input

### Not Found Errors
- Task not found by ID: Show error toast
- Empty task list: Show helpful "Add your first task" message

