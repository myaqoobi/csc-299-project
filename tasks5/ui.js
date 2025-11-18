/**
 * UI Layer for Task Manager
 * Handles all DOM manipulation and rendering
 */

const UI = {
    /**
     * Render the task list
     * @param {Array} tasks - Array of task objects to render
     */
    renderTaskList(tasks) {
        const taskList = document.getElementById('task-list');
        const emptyState = document.getElementById('empty-state');
        
        // Clear existing tasks
        taskList.innerHTML = '';
        
        // Show/hide empty state
        if (tasks.length === 0) {
            emptyState.style.display = 'block';
            taskList.style.display = 'none';
            return;
        } else {
            emptyState.style.display = 'none';
            taskList.style.display = 'flex';
        }
        
        // Render each task
        tasks.forEach(task => {
            const taskCard = this.createTaskCard(task);
            taskList.appendChild(taskCard);
        });
    },
    
    /**
     * Create a task card element
     * @param {Object} task - Task object
     * @returns {HTMLElement} Task card element
     */
    createTaskCard(task) {
        const card = document.createElement('div');
        card.className = `task-card priority-${task.priority}`;
        if (task.status === 'complete') {
            card.classList.add('completed');
        }
        card.dataset.taskId = task.id;
        
        // Task header (checkbox + content + actions)
        const header = document.createElement('div');
        header.className = 'task-header';
        
        // Checkbox
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'task-checkbox';
        checkbox.checked = task.status === 'complete';
        checkbox.addEventListener('change', () => {
            window.app.handleToggleComplete(task.id);
        });
        
        // Content
        const content = document.createElement('div');
        content.className = 'task-content';
        
        // Title
        const title = document.createElement('h3');
        title.className = 'task-title';
        if (task.status === 'complete') {
            title.classList.add('completed');
        }
        title.textContent = task.title;
        content.appendChild(title);
        
        // Description (if exists)
        if (task.description) {
            const description = document.createElement('p');
            description.className = 'task-description';
            description.textContent = task.description;
            content.appendChild(description);
        }
        
        // Meta information (priority, due date, tags)
        const meta = this.createTaskMeta(task);
        content.appendChild(meta);
        
        // Actions
        const actions = document.createElement('div');
        actions.className = 'task-actions';
        
        const editBtn = document.createElement('button');
        editBtn.className = 'btn btn-secondary btn-small';
        editBtn.textContent = 'Edit';
        editBtn.addEventListener('click', () => {
            window.app.handleEditTask(task.id);
        });
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-danger btn-small';
        deleteBtn.textContent = 'Delete';
        deleteBtn.addEventListener('click', () => {
            window.app.handleDeleteTask(task.id);
        });
        
        actions.appendChild(editBtn);
        actions.appendChild(deleteBtn);
        
        // Assemble header
        header.appendChild(checkbox);
        header.appendChild(content);
        header.appendChild(actions);
        
        card.appendChild(header);
        
        return card;
    },
    
    /**
     * Create task meta information (badges)
     * @param {Object} task - Task object
     * @returns {HTMLElement} Meta container element
     */
    createTaskMeta(task) {
        const meta = document.createElement('div');
        meta.className = 'task-meta';
        
        // Priority badge
        const priorityBadge = document.createElement('span');
        priorityBadge.className = `badge badge-priority ${task.priority}`;
        priorityBadge.textContent = task.priority.toUpperCase();
        meta.appendChild(priorityBadge);
        
        // Due date badge (if exists)
        if (task.dueDate) {
            const dueBadge = document.createElement('span');
            dueBadge.className = 'badge badge-due';
            
            const overdue = isOverdue(task.dueDate);
            if (overdue && task.status === 'incomplete') {
                dueBadge.classList.add('overdue');
            }
            
            dueBadge.textContent = `📅 ${formatDate(task.dueDate)}`;
            meta.appendChild(dueBadge);
        }
        
        // Tag badges
        task.tags.forEach(tag => {
            const tagBadge = document.createElement('span');
            tagBadge.className = 'badge badge-tag';
            tagBadge.textContent = `#${tag}`;
            meta.appendChild(tagBadge);
        });
        
        return meta;
    },
    
    /**
     * Render statistics
     * @param {Object} stats - Statistics object
     */
    renderStatistics(stats) {
        document.getElementById('stat-total').textContent = stats.total;
        document.getElementById('stat-active').textContent = stats.active;
        document.getElementById('stat-completed').textContent = stats.completed;
    },
    
    /**
     * Show task form for adding or editing
     * @param {Object|null} task - Task object for editing, null for new task
     */
    showTaskForm(task = null) {
        const form = document.getElementById('task-form');
        const titleInput = document.getElementById('task-title');
        const descriptionInput = document.getElementById('task-description');
        const prioritySelect = document.getElementById('task-priority');
        const dueDateInput = document.getElementById('task-due-date');
        const tagsInput = document.getElementById('task-tags');
        const taskIdInput = document.getElementById('task-id');
        const submitBtn = document.getElementById('submit-text');
        const detailsSection = document.getElementById('form-details');
        const toggleBtn = document.getElementById('toggle-details');
        
        if (task) {
            // Edit mode
            titleInput.value = task.title;
            descriptionInput.value = task.description || '';
            prioritySelect.value = task.priority;
            dueDateInput.value = task.dueDate || '';
            tagsInput.value = task.tags.join(', ');
            taskIdInput.value = task.id;
            submitBtn.textContent = 'Update Task';
            
            // Show details section
            detailsSection.style.display = 'flex';
            toggleBtn.textContent = '- Hide Details';
            
            // Scroll to form
            form.scrollIntoView({ behavior: 'smooth', block: 'start' });
            titleInput.focus();
        } else {
            // Add mode (already default state)
            form.reset();
            taskIdInput.value = '';
            submitBtn.textContent = 'Add Task';
        }
    },
    
    /**
     * Clear/reset the task form
     */
    clearTaskForm() {
        const form = document.getElementById('task-form');
        form.reset();
        document.getElementById('task-id').value = '';
        document.getElementById('submit-text').textContent = 'Add Task';
        
        // Hide details section
        const detailsSection = document.getElementById('form-details');
        const toggleBtn = document.getElementById('toggle-details');
        detailsSection.style.display = 'none';
        toggleBtn.textContent = '+ Add Details';
    },
    
    /**
     * Show confirmation dialog
     * @param {string} message - Confirmation message
     * @returns {Promise<boolean>} Promise that resolves to true if confirmed
     */
    showConfirmDialog(message) {
        return new Promise((resolve) => {
            const dialog = document.getElementById('confirm-dialog');
            const messageEl = document.getElementById('confirm-message');
            const okBtn = document.getElementById('confirm-ok');
            const cancelBtn = document.getElementById('confirm-cancel');
            
            messageEl.textContent = message;
            dialog.style.display = 'flex';
            
            const handleOk = () => {
                dialog.style.display = 'none';
                cleanup();
                resolve(true);
            };
            
            const handleCancel = () => {
                dialog.style.display = 'none';
                cleanup();
                resolve(false);
            };
            
            const cleanup = () => {
                okBtn.removeEventListener('click', handleOk);
                cancelBtn.removeEventListener('click', handleCancel);
            };
            
            okBtn.addEventListener('click', handleOk);
            cancelBtn.addEventListener('click', handleCancel);
        });
    },
    
    /**
     * Show toast notification
     * @param {string} message - Notification message
     * @param {string} type - Type: 'success' or 'error'
     * @param {number} duration - Duration in ms (default 3000)
     */
    showToast(message, type = 'success', duration = 3000) {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.style.display = 'block';
        
        setTimeout(() => {
            toast.style.display = 'none';
        }, duration);
    },
    
    /**
     * Show error message
     * @param {string} message - Error message
     */
    showError(message) {
        this.showToast(message, 'error', 4000);
    },
    
    /**
     * Show success message
     * @param {string} message - Success message
     */
    showSuccess(message) {
        this.showToast(message, 'success', 2000);
    },
    
    /**
     * Show export options dialog
     * @returns {Promise<string|null>} Selected format ('json' or 'csv') or null if cancelled
     */
    async showExportDialog() {
        const format = prompt('Export format:\n\nType "json" for JSON backup\nType "csv" for spreadsheet');
        
        if (!format) return null;
        
        const normalized = format.toLowerCase().trim();
        if (normalized === 'json' || normalized === 'csv') {
            return normalized;
        }
        
        this.showError('Invalid format. Please choose "json" or "csv".');
        return null;
    }
};

