/**
 * Task Manager - Core Business Logic
 * Handles all task-related operations (CRUD, filtering, statistics)
 */

class TaskManager {
    constructor() {
        this.tasks = [];
        this.loadTasks();
    }
    
    /**
     * Load tasks from storage
     */
    loadTasks() {
        this.tasks = Storage.loadTasks();
    }
    
    /**
     * Save tasks to storage
     * @returns {boolean} True if save successful
     */
    saveTasks() {
        return Storage.saveTasks(this.tasks);
    }
    
    /**
     * Create a new task
     * @param {Object} taskData - Task data object
     * @returns {Object} Created task object
     */
    createTask(taskData) {
        // Validate required fields
        if (!taskData.title || !taskData.title.trim()) {
            throw new Error('Task title is required');
        }
        
        // Validate priority
        const validPriorities = ['low', 'medium', 'high'];
        if (taskData.priority && !validPriorities.includes(taskData.priority)) {
            throw new Error('Invalid priority value');
        }
        
        // Create task object
        const task = {
            id: generateId(),
            title: sanitizeHTML(taskData.title.trim()),
            description: sanitizeHTML(taskData.description?.trim() || ''),
            status: 'incomplete',
            priority: taskData.priority || 'medium',
            dueDate: taskData.dueDate || null,
            tags: Array.isArray(taskData.tags) ? taskData.tags : parseTags(taskData.tags || ''),
            createdAt: new Date().toISOString(),
            completedAt: null
        };
        
        // Add to tasks array
        this.tasks.push(task);
        this.saveTasks();
        
        return task;
    }
    
    /**
     * Get task by ID
     * @param {string} id - Task ID
     * @returns {Object|null} Task object or null if not found
     */
    getTaskById(id) {
        return this.tasks.find(task => task.id === id) || null;
    }
    
    /**
     * Get all tasks
     * @returns {Array} Array of all tasks
     */
    getAllTasks() {
        return [...this.tasks]; // Return copy to prevent direct modification
    }
    
    /**
     * Update a task
     * @param {string} id - Task ID
     * @param {Object} updates - Fields to update
     * @returns {Object} Updated task object
     */
    updateTask(id, updates) {
        const taskIndex = this.tasks.findIndex(task => task.id === id);
        
        if (taskIndex === -1) {
            throw new Error('Task not found');
        }
        
        const task = this.tasks[taskIndex];
        
        // Prevent changing ID and createdAt
        delete updates.id;
        delete updates.createdAt;
        
        // Validate title if being updated
        if (updates.title !== undefined && !updates.title.trim()) {
            throw new Error('Task title cannot be empty');
        }
        
        // Validate priority if being updated
        if (updates.priority !== undefined) {
            const validPriorities = ['low', 'medium', 'high'];
            if (!validPriorities.includes(updates.priority)) {
                throw new Error('Invalid priority value');
            }
        }
        
        // Sanitize text fields
        if (updates.title) updates.title = sanitizeHTML(updates.title.trim());
        if (updates.description !== undefined) {
            updates.description = sanitizeHTML(updates.description?.trim() || '');
        }
        
        // Parse tags if provided as string
        if (updates.tags && typeof updates.tags === 'string') {
            updates.tags = parseTags(updates.tags);
        }
        
        // Merge updates
        this.tasks[taskIndex] = { ...task, ...updates };
        this.saveTasks();
        
        return this.tasks[taskIndex];
    }
    
    /**
     * Delete a task
     * @param {string} id - Task ID
     * @returns {boolean} True if deleted successfully
     */
    deleteTask(id) {
        const taskIndex = this.tasks.findIndex(task => task.id === id);
        
        if (taskIndex === -1) {
            throw new Error('Task not found');
        }
        
        this.tasks.splice(taskIndex, 1);
        this.saveTasks();
        
        return true;
    }
    
    /**
     * Mark task as complete
     * @param {string} id - Task ID
     * @returns {Object} Updated task object
     */
    completeTask(id) {
        const task = this.getTaskById(id);
        
        if (!task) {
            throw new Error('Task not found');
        }
        
        return this.updateTask(id, {
            status: 'complete',
            completedAt: new Date().toISOString()
        });
    }
    
    /**
     * Mark task as incomplete
     * @param {string} id - Task ID
     * @returns {Object} Updated task object
     */
    uncompleteTask(id) {
        const task = this.getTaskById(id);
        
        if (!task) {
            throw new Error('Task not found');
        }
        
        return this.updateTask(id, {
            status: 'incomplete',
            completedAt: null
        });
    }
    
    /**
     * Toggle task completion status
     * @param {string} id - Task ID
     * @returns {Object} Updated task object
     */
    toggleComplete(id) {
        const task = this.getTaskById(id);
        
        if (!task) {
            throw new Error('Task not found');
        }
        
        if (task.status === 'complete') {
            return this.uncompleteTask(id);
        } else {
            return this.completeTask(id);
        }
    }
    
    /**
     * Filter tasks based on criteria
     * @param {Object} criteria - Filter criteria
     * @returns {Array} Filtered tasks array
     */
    filterTasks(criteria = {}) {
        let filtered = this.getAllTasks();
        
        // Filter by status
        if (criteria.status && criteria.status !== 'all') {
            filtered = filtered.filter(task => task.status === criteria.status);
        }
        
        // Filter by priority
        if (criteria.priority && criteria.priority !== 'all') {
            filtered = filtered.filter(task => task.priority === criteria.priority);
        }
        
        // Filter overdue tasks
        if (criteria.overdue) {
            filtered = filtered.filter(task => 
                task.status === 'incomplete' && task.dueDate && isOverdue(task.dueDate)
            );
        }
        
        // Filter by tag
        if (criteria.tag) {
            filtered = filtered.filter(task => task.tags.includes(criteria.tag));
        }
        
        // Search in title, description, and tags
        if (criteria.search) {
            const query = criteria.search.toLowerCase();
            filtered = filtered.filter(task => {
                return (
                    task.title.toLowerCase().includes(query) ||
                    task.description.toLowerCase().includes(query) ||
                    task.tags.some(tag => tag.toLowerCase().includes(query))
                );
            });
        }
        
        return filtered;
    }
    
    /**
     * Get task statistics
     * @returns {Object} Statistics object
     */
    getStatistics() {
        const stats = {
            total: this.tasks.length,
            active: 0,
            completed: 0,
            overdue: 0,
            dueToday: 0,
            dueSoon: 0,
            highPriority: 0,
            byPriority: { high: 0, medium: 0, low: 0 },
            byTag: {}
        };
        
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        const sevenDaysFromNow = new Date(today);
        sevenDaysFromNow.setDate(sevenDaysFromNow.getDate() + 7);
        
        this.tasks.forEach(task => {
            // Status counts
            if (task.status === 'complete') {
                stats.completed++;
            } else {
                stats.active++;
            }
            
            // Priority counts
            stats.byPriority[task.priority]++;
            
            if (task.status === 'incomplete' && task.priority === 'high') {
                stats.highPriority++;
            }
            
            // Due date checks (only for incomplete tasks)
            if (task.status === 'incomplete' && task.dueDate) {
                const dueDate = new Date(task.dueDate + 'T00:00:00');
                dueDate.setHours(0, 0, 0, 0);
                
                if (dueDate < today) {
                    stats.overdue++;
                } else if (dueDate.getTime() === today.getTime()) {
                    stats.dueToday++;
                } else if (dueDate <= sevenDaysFromNow) {
                    stats.dueSoon++;
                }
            }
            
            // Tag counts
            task.tags.forEach(tag => {
                stats.byTag[tag] = (stats.byTag[tag] || 0) + 1;
            });
        });
        
        return stats;
    }
    
    /**
     * Get all unique tags from all tasks
     * @returns {Array} Array of unique tag strings
     */
    getAllTags() {
        const tagSet = new Set();
        this.tasks.forEach(task => {
            task.tags.forEach(tag => tagSet.add(tag));
        });
        return Array.from(tagSet).sort();
    }
}

