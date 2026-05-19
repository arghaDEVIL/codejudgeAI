import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merge Tailwind CSS classes with proper precedence
 */
export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

/**
 * Format date to relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(date) {
    const now = new Date();
    const diff = now - new Date(date);
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return "just now";
}

/**
 * Format execution time
 */
export function formatExecutionTime(ms) {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
}

/**
 * Format memory usage
 */
export function formatMemory(mb) {
    if (mb < 1) return `${(mb * 1024).toFixed(0)}KB`;
    return `${mb.toFixed(2)}MB`;
}

/**
 * Get difficulty color
 */
export function getDifficultyColor(difficulty) {
    const colors = {
        Easy: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
        Medium: "text-amber-400 bg-amber-500/10 border-amber-500/20",
        Hard: "text-red-400 bg-red-500/10 border-red-500/20",
    };
    return colors[difficulty] || colors.Medium;
}

/**
 * Get status color
 */
export function getStatusColor(status) {
    const colors = {
        Accepted: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
        "Wrong Answer": "text-red-400 bg-red-500/10 border-red-500/20",
        "Time Limit Exceeded": "text-amber-400 bg-amber-500/10 border-amber-500/20",
        "Runtime Error": "text-orange-400 bg-orange-500/10 border-orange-500/20",
        "Compilation Error": "text-purple-400 bg-purple-500/10 border-purple-500/20",
        Pending: "text-blue-400 bg-blue-500/10 border-blue-500/20",
    };
    return colors[status] || colors.Pending;
}

/**
 * Truncate text
 */
export function truncate(text, length = 50) {
    if (!text) return "";
    if (text.length <= length) return text;
    return text.substring(0, length) + "...";
}

/**
 * Debounce function
 */
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
