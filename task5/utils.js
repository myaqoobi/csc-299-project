/**
 * Utility Functions for Task Manager
 * Shared helper functions used across the application
 */

/**
 * Generate a unique ID for tasks
 * Format: task_{timestamp}_{randomHex}
 */
function generateId() {
    const timestamp = Date.now();
    const random = Math.random().toString(16).substring(2, 8);
    return `task_${timestamp}_${random}`;
}

/**
 * Format date for display
 * @param {string} dateString - ISO date string (YYYY-MM-DD)
 * @returns {string} Formatted date string
 */
function formatDate(dateString) {
    if (!dateString) return '';
    
    const date = new Date(dateString + 'T00:00:00'); // Treat as local date
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    date.setHours(0, 0, 0, 0);
    
    if (date.getTime() === today.getTime()) {
        return 'Today';
    } else if (date.getTime() === tomorrow.getTime()) {
        return 'Tomorrow';
    } else if (date.getTime() === yesterday.getTime()) {
        return 'Yesterday';
    } else {
        // Format as readable date
        const options = { month: 'short', day: 'numeric', year: 'numeric' };
        return date.toLocaleDateString(undefined, options);
    }
}

/**
 * Check if a date is overdue (in the past)
 * @param {string} dueDateString - ISO date string (YYYY-MM-DD)
 * @returns {boolean} True if overdue
 */
function isOverdue(dueDateString) {
    if (!dueDateString) return false;
    
    const dueDate = new Date(dueDateString + 'T00:00:00');
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    dueDate.setHours(0, 0, 0, 0);
    
    return dueDate < today;
}

/**
 * Sanitize HTML to prevent XSS attacks
 * @param {string} str - User input string
 * @returns {string} Sanitized string
 */
function sanitizeHTML(str) {
    if (typeof str !== 'string') return '';
    
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/**
 * Parse comma-separated tags into array
 * @param {string} tagString - Comma-separated tag string
 * @returns {string[]} Array of trimmed, unique tags
 */
function parseTags(tagString) {
    if (!tagString || typeof tagString !== 'string') return [];
    
    return tagString
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0)
        .filter((tag, index, self) => self.indexOf(tag) === index); // Remove duplicates
}

/**
 * Debounce function to limit rate of function execution
 * @param {Function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, delay = 300) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Validate email format (for future use)
 * @param {string} email - Email string to validate
 * @returns {boolean} True if valid email format
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Get relative time string (e.g., "2 days ago")
 * @param {string} dateString - ISO timestamp string
 * @returns {string} Relative time string
 */
function getRelativeTime(dateString) {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffSecs = Math.floor(diffMs / 1000);
    const diffMins = Math.floor(diffSecs / 60);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffSecs < 60) {
        return 'Just now';
    } else if (diffMins < 60) {
        return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else if (diffDays < 7) {
        return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    } else {
        return formatDate(dateString.split('T')[0]);
    }
}

/**
 * Escape CSV special characters
 * @param {string} str - String to escape
 * @returns {string} Escaped string
 */
function escapeCSV(str) {
    if (typeof str !== 'string') return '';
    if (str.includes('"') || str.includes(',') || str.includes('\n')) {
        return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
}

