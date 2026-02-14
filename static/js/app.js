/**
 * Job Application Tracker - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            const icon = navToggle.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (navMenu && navMenu.classList.contains('active')) {
            if (!navMenu.contains(e.target) && !navToggle.contains(e.target)) {
                navMenu.classList.remove('active');
                const icon = navToggle.querySelector('i');
                icon.classList.add('fa-bars');
                icon.classList.remove('fa-times');
            }
        }
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Confirm delete on all delete buttons
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const message = this.dataset.confirm || '¿Estás seguro?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Initialize charts if they exist
    initCharts();

    // Initialize tooltips
    initTooltips();

    // Initialize date pickers with today as default
    initDatePickers();

    // Initialize search filters
    initSearchFilters();
});

/**
 * Initialize any charts on the page
 */
function initCharts() {
    // Charts would be initialized here if using a charting library
    // For now, we use CSS-based visualizations
}

/**
 * Initialize tooltips
 */
function initTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', function(e) {
            const text = this.dataset.tooltip;
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = text;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
            
            this._tooltip = tooltip;
        });
        
        trigger.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

/**
 * Initialize date pickers
 */
function initDatePickers() {
    const today = new Date().toISOString().split('T')[0];
    
    // Set max date to today for postulacion dates
    const postulacionDates = document.querySelectorAll('input[name="fecha_postulacion"]');
    postulacionDates.forEach(input => {
        input.max = today;
        if (!input.value) {
            input.value = today;
        }
    });

    // Set min date to today for seguimiento dates
    const seguimientoDates = document.querySelectorAll('input[name="fecha_seguimiento"]');
    seguimientoDates.forEach(input => {
        input.min = today;
    });
}

/**
 * Initialize search filters with debounce
 */
function initSearchFilters() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const form = this.closest('form');
                if (form && form.dataset.autoSubmit) {
                    form.submit();
                }
            }, 500);
        });
    });
}

/**
 * Toggle filter visibility
 */
function toggleFilters() {
    const filtersCard = document.querySelector('.filters-card');
    if (filtersCard) {
        filtersCard.classList.toggle('collapsed');
    }
}

/**
 * Export data to CSV
 */
function exportToCSV(data, filename) {
    const csvContent = convertToCSV(data);
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

/**
 * Convert array of objects to CSV string
 */
function convertToCSV(data) {
    if (!data || !data.length) return '';
    
    const headers = Object.keys(data[0]);
    const rows = data.map(obj => 
        headers.map(header => {
            let cell = obj[header] || '';
            // Escape quotes and wrap in quotes if needed
            if (typeof cell === 'string' && (cell.includes(',') || cell.includes('"') || cell.includes('\n'))) {
                cell = '"' + cell.replace(/"/g, '""') + '"';
            }
            return cell;
        }).join(',')
    );
    
    return [headers.join(','), ...rows].join('\n');
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copiado al portapapeles', 'success');
    } catch (err) {
        showNotification('Error al copiar', 'error');
    }
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    requestAnimationFrame(() => {
        notification.classList.add('show');
    });
    
    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Quick status change with AJAX
 */
async function quickStatusChange(postulacionId, newStatus) {
    try {
        const formData = new FormData();
        formData.append('nuevo_estado', newStatus);
        
        const response = await fetch(`/postulaciones/${postulacionId}/cambiar-estado`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showNotification(`Estado actualizado a: ${newStatus}`, 'success');
            // Reload page after a short delay
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification('Error al actualizar el estado', 'error');
        }
    } catch (error) {
        showNotification('Error de conexión', 'error');
        console.error(error);
    }
}

/**
 * Refresh dashboard stats
 */
async function refreshStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        // Update stat cards
        document.querySelectorAll('[data-stat]').forEach(el => {
            const statName = el.dataset.stat;
            if (stats[statName] !== undefined) {
                el.textContent = stats[statName];
            }
        });
        
        showNotification('Estadísticas actualizadas', 'success');
    } catch (error) {
        console.error('Error refreshing stats:', error);
    }
}

/**
 * Calculate days between dates
 */
function daysBetween(date1, date2) {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    const diffTime = Math.abs(d2 - d1);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

/**
 * Add CSS styles for notifications
 */
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 16px 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 12px;
        transform: translateX(150%);
        transition: transform 0.3s ease;
        z-index: 1000;
        max-width: 400px;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 4px solid #22c55e;
    }
    
    .notification-success i {
        color: #22c55e;
    }
    
    .notification-error {
        border-left: 4px solid #ef4444;
    }
    
    .notification-error i {
        color: #ef4444;
    }
    
    .notification-info {
        border-left: 4px solid #0ea5e9;
    }
    
    .notification-info i {
        color: #0ea5e9;
    }
    
    .tooltip {
        position: absolute;
        background: #1e293b;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        white-space: nowrap;
        z-index: 1000;
        pointer-events: none;
    }
    
    .tooltip::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 6px solid transparent;
        border-top-color: #1e293b;
    }
`;
document.head.appendChild(notificationStyles);
