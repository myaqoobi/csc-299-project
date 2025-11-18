/**
 * Storage Layer for Task Manager
 * Handles localStorage operations with error handling
 */

const Storage = {
    STORAGE_KEY: 'taskManager_tasks',
    
    /**
     * Check if localStorage is available
     * @returns {boolean} True if localStorage is available
     */
    isAvailable() {
        try {
            const test = '__storage_test__';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch (e) {
            return false;
        }
    },
    
    /**
     * Load tasks from localStorage
     * @returns {Array} Array of task objects, empty array on error
     */
    loadTasks() {
        if (!this.isAvailable()) {
            console.warn('localStorage is not available. Running in memory mode.');
            return [];
        }
        
        try {
            const data = localStorage.getItem(this.STORAGE_KEY);
            if (!data) {
                return [];
            }
            
            const tasks = JSON.parse(data);
            if (!Array.isArray(tasks)) {
                console.error('Stored data is not an array. Returning empty array.');
                return [];
            }
            
            return tasks;
        } catch (error) {
            console.error('Error loading tasks from localStorage:', error);
            
            // Try to preserve corrupt data
            try {
                const corruptData = localStorage.getItem(this.STORAGE_KEY);
                if (corruptData) {
                    localStorage.setItem(this.STORAGE_KEY + '_corrupt_backup', corruptData);
                    console.log('Corrupt data backed up to:', this.STORAGE_KEY + '_corrupt_backup');
                }
            } catch (e) {
                console.error('Could not backup corrupt data:', e);
            }
            
            return [];
        }
    },
    
    /**
     * Save tasks to localStorage
     * @param {Array} tasks - Array of task objects
     * @returns {boolean} True if save successful
     */
    saveTasks(tasks) {
        if (!this.isAvailable()) {
            console.warn('localStorage is not available. Data will not persist.');
            return false;
        }
        
        if (!Array.isArray(tasks)) {
            console.error('saveTasks requires an array');
            return false;
        }
        
        try {
            const data = JSON.stringify(tasks);
            localStorage.setItem(this.STORAGE_KEY, data);
            return true;
        } catch (error) {
            if (error.name === 'QuotaExceededError') {
                console.error('localStorage quota exceeded!');
                alert('Storage is full! Please export your tasks and delete old ones.');
            } else {
                console.error('Error saving tasks to localStorage:', error);
            }
            return false;
        }
    },
    
    /**
     * Export tasks as JSON file
     * @param {Array} tasks - Array of task objects
     * @returns {boolean} True if export successful
     */
    exportToJSON(tasks) {
        try {
            const data = JSON.stringify(tasks, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = `tasks-export-${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            return true;
        } catch (error) {
            console.error('Error exporting to JSON:', error);
            return false;
        }
    },
    
    /**
     * Export tasks as CSV file
     * @param {Array} tasks - Array of task objects
     * @returns {boolean} True if export successful
     */
    exportToCSV(tasks) {
        try {
            // CSV Header
            const headers = ['Title', 'Description', 'Status', 'Priority', 'Due Date', 'Tags', 'Created', 'Completed'];
            const csvLines = [headers.join(',')];
            
            // CSV Rows
            tasks.forEach(task => {
                const row = [
                    escapeCSV(task.title),
                    escapeCSV(task.description || ''),
                    escapeCSV(task.status),
                    escapeCSV(task.priority),
                    escapeCSV(task.dueDate || ''),
                    escapeCSV(task.tags.join(', ')),
                    escapeCSV(task.createdAt),
                    escapeCSV(task.completedAt || '')
                ];
                csvLines.push(row.join(','));
            });
            
            const csvContent = csvLines.join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = `tasks-export-${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            return true;
        } catch (error) {
            console.error('Error exporting to CSV:', error);
            return false;
        }
    },
    
    /**
     * Import tasks from JSON string
     * @param {string} jsonString - JSON string containing tasks array
     * @returns {Array|null} Parsed tasks array or null on error
     */
    importFromJSON(jsonString) {
        try {
            const tasks = JSON.parse(jsonString);
            
            if (!Array.isArray(tasks)) {
                throw new Error('Invalid format: expected array of tasks');
            }
            
            // Basic validation
            tasks.forEach((task, index) => {
                if (!task.id || !task.title) {
                    throw new Error(`Task at index ${index} is missing required fields`);
                }
            });
            
            return tasks;
        } catch (error) {
            console.error('Error importing JSON:', error);
            return null;
        }
    },
    
    /**
     * Clear all task data
     * @returns {boolean} True if successful
     */
    clearAllData() {
        if (!this.isAvailable()) {
            return false;
        }
        
        try {
            localStorage.removeItem(this.STORAGE_KEY);
            return true;
        } catch (error) {
            console.error('Error clearing data:', error);
            return false;
        }
    },
    
    /**
     * Get storage usage information
     * @returns {Object} Storage usage stats
     */
    getStorageInfo() {
        if (!this.isAvailable()) {
            return { available: false };
        }
        
        try {
            const data = localStorage.getItem(this.STORAGE_KEY);
            const bytes = data ? new Blob([data]).size : 0;
            const kb = (bytes / 1024).toFixed(2);
            
            return {
                available: true,
                bytes: bytes,
                kb: kb,
                taskCount: data ? JSON.parse(data).length : 0
            };
        } catch (error) {
            console.error('Error getting storage info:', error);
            return { available: true, error: error.message };
        }
    }
};

