/**
 * Main Application File
 * Initializes the app and coordinates all components
 */

class App {
    constructor() {
        this.taskManager = null;
        this.currentFilters = {
            status: 'all',
            priority: 'all',
            overdue: false,
            tag: null,
            search: ''
        };
    }
    
    /**
     * Initialize the application
     */
    init() {
        // Initialize task manager
        this.taskManager = new TaskManager();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Initial render
        this.render();
        
        console.log('Task Manager initialized successfully!');
        
        // Show storage info in console
        const storageInfo = Storage.getStorageInfo();
        if (storageInfo.available) {
            console.log(`Storage: ${storageInfo.kb} KB used, ${storageInfo.taskCount} tasks`);
        } else {
            console.warn('Running in memory mode - data will not persist');
            UI.showToast('localStorage is not available. Running in memory mode.', 'error', 5000);
        }
    }
    
    /**
     * Setup all event listeners
     */
    setupEventListeners() {
        // Task form submission
        const taskForm = document.getElementById('task-form');
        taskForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit();
        });
        
        // Toggle details button
        const toggleDetailsBtn = document.getElementById('toggle-details');
        toggleDetailsBtn.addEventListener('click', () => {
            const detailsSection = document.getElementById('form-details');
            const isVisible = detailsSection.style.display !== 'none';
            detailsSection.style.display = isVisible ? 'none' : 'flex';
            toggleDetailsBtn.textContent = isVisible ? '+ Add Details' : '- Hide Details';
        });
        
        // Search input (debounced)
        const searchInput = document.getElementById('search-input');
        searchInput.addEventListener('input', debounce((e) => {
            this.currentFilters.search = e.target.value;
            this.render();
        }, 300));
        
        // Filter dropdowns
        const statusFilter = document.getElementById('filter-status');
        statusFilter.addEventListener('change', (e) => {
            this.currentFilters.status = e.target.value;
            this.render();
        });
        
        const priorityFilter = document.getElementById('filter-priority');
        priorityFilter.addEventListener('change', (e) => {
            this.currentFilters.priority = e.target.value;
            this.render();
        });
        
        // Overdue checkbox
        const overdueCheckbox = document.getElementById('filter-overdue');
        overdueCheckbox.addEventListener('change', (e) => {
            this.currentFilters.overdue = e.target.checked;
            this.render();
        });
        
        // Clear filters button
        const clearFiltersBtn = document.getElementById('clear-filters');
        clearFiltersBtn.addEventListener('click', () => {
            this.clearFilters();
        });
        
        // Export button
        const exportBtn = document.getElementById('export-btn');
        exportBtn.addEventListener('click', () => {
            this.handleExport();
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Escape to clear form
            if (e.key === 'Escape') {
                UI.clearTaskForm();
            }
        });
    }
    
    /**
     * Handle form submission (add or update task)
     */
    handleFormSubmit() {
        try {
            // Get form data
            const taskId = document.getElementById('task-id').value;
            const title = document.getElementById('task-title').value;
            const description = document.getElementById('task-description').value;
            const priority = document.getElementById('task-priority').value;
            const dueDate = document.getElementById('task-due-date').value;
            const tags = document.getElementById('task-tags').value;
            
            const taskData = {
                title,
                description,
                priority,
                dueDate: dueDate || null,
                tags
            };
            
            if (taskId) {
                // Update existing task
                this.taskManager.updateTask(taskId, taskData);
                UI.showSuccess('Task updated successfully!');
            } else {
                // Create new task
                this.taskManager.createTask(taskData);
                UI.showSuccess('Task created successfully!');
            }
            
            // Clear form and re-render
            UI.clearTaskForm();
            this.render();
            
            // Focus back on title input for quick entry
            document.getElementById('task-title').focus();
            
        } catch (error) {
            console.error('Error submitting form:', error);
            UI.showError(error.message);
        }
    }
    
    /**
     * Handle task completion toggle
     * @param {string} taskId - Task ID
     */
    handleToggleComplete(taskId) {
        try {
            this.taskManager.toggleComplete(taskId);
            this.render();
        } catch (error) {
            console.error('Error toggling task completion:', error);
            UI.showError(error.message);
        }
    }
    
    /**
     * Handle edit task button click
     * @param {string} taskId - Task ID
     */
    handleEditTask(taskId) {
        try {
            const task = this.taskManager.getTaskById(taskId);
            if (task) {
                UI.showTaskForm(task);
            }
        } catch (error) {
            console.error('Error loading task for edit:', error);
            UI.showError(error.message);
        }
    }
    
    /**
     * Handle delete task button click
     * @param {string} taskId - Task ID
     */
    async handleDeleteTask(taskId) {
        try {
            const task = this.taskManager.getTaskById(taskId);
            if (!task) return;
            
            const confirmed = await UI.showConfirmDialog(
                `Are you sure you want to delete "${task.title}"? This action cannot be undone.`
            );
            
            if (confirmed) {
                this.taskManager.deleteTask(taskId);
                UI.showSuccess('Task deleted successfully!');
                this.render();
            }
        } catch (error) {
            console.error('Error deleting task:', error);
            UI.showError(error.message);
        }
    }
    
    /**
     * Handle export button click
     */
    async handleExport() {
        try {
            const format = await UI.showExportDialog();
            
            if (!format) return;
            
            const tasks = this.taskManager.getAllTasks();
            
            if (tasks.length === 0) {
                UI.showError('No tasks to export!');
                return;
            }
            
            let success = false;
            
            if (format === 'json') {
                success = Storage.exportToJSON(tasks);
            } else if (format === 'csv') {
                success = Storage.exportToCSV(tasks);
            }
            
            if (success) {
                UI.showSuccess(`Tasks exported successfully as ${format.toUpperCase()}!`);
            } else {
                UI.showError('Export failed. Please try again.');
            }
        } catch (error) {
            console.error('Error exporting tasks:', error);
            UI.showError('Export failed: ' + error.message);
        }
    }
    
    /**
     * Clear all filters and reset view
     */
    clearFilters() {
        this.currentFilters = {
            status: 'all',
            priority: 'all',
            overdue: false,
            tag: null,
            search: ''
        };
        
        // Reset filter UI
        document.getElementById('filter-status').value = 'all';
        document.getElementById('filter-priority').value = 'all';
        document.getElementById('filter-overdue').checked = false;
        document.getElementById('search-input').value = '';
        
        this.render();
        UI.showSuccess('Filters cleared!');
    }
    
    /**
     * Render the entire UI
     */
    render() {
        // Get filtered tasks
        const filteredTasks = this.taskManager.filterTasks(this.currentFilters);
        
        // Render task list
        UI.renderTaskList(filteredTasks);
        
        // Render statistics
        const stats = this.taskManager.getStatistics();
        UI.renderStatistics(stats);
    }
}

// Initialize app when DOM is ready
let app;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        app = new App();
        app.init();
        window.app = app; // Make available globally for event handlers
    });
} else {
    app = new App();
    app.init();
    window.app = app;
}

