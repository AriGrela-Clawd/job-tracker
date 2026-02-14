// Job Application Tracker - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // Confirm delete functionality
    window.confirmDelete = function(message) {
        return confirm(message || '¿Estás seguro de que deseas eliminar este elemento? Esta acción no se puede deshacer.');
    };
    
    // Table row hover effect enhancement
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.cursor = 'pointer';
        });
        
        // Make entire row clickable if it has a link
        const link = row.querySelector('a');
        if (link) {
            row.addEventListener('click', function(e) {
                // Don't navigate if clicking on buttons or forms
                if (e.target.closest('button') || e.target.closest('form')) {
                    return;
                }
                window.location.href = link.href;
            });
        }
    });
    
    // Search debounce
    const searchInputs = document.querySelectorAll('input[name="search"]');
    searchInputs.forEach(input => {
        let debounceTimer;
        input.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                // Optional: auto-submit search form after delay
                // this.closest('form').submit();
            }, 500);
        });
    });
    
    // Status badge color updates
    updateStatusBadges();
    
    // Initialize tooltips (if any)
    initializeTooltips();
    
    // Date input helpers
    initializeDateHelpers();
});

// Update status badges with appropriate colors
function updateStatusBadges() {
    const statusMap = {
        'Postulado': 'status-postulado',
        'En revisión': 'status-en-revisión',
        'Entrevista': 'status-entrevista',
        'Oferta': 'status-oferta',
        'Rechazado': 'status-rechazado',
        'Aceptado': 'status-aceptado',
        'Sin respuesta': 'status-sin-respuesta'
    };
    
    document.querySelectorAll('.status-badge').forEach(badge => {
        const text = badge.textContent.trim();
        if (statusMap[text]) {
            badge.className = `status-badge ${statusMap[text]}`;
        }
    });
}

// Initialize simple tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
            tooltip.style.opacity = '1';
            
            this._tooltip = tooltip;
        });
        
        el.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Date input helpers
function initializeDateHelpers() {
    // Set max date to today for date inputs that need it
    const today = new Date().toISOString().split('T')[0];
    
    document.querySelectorAll('input[type="date"]').forEach(input => {
        // Add calendar icon click handler
        input.addEventListener('click', function() {
            this.showPicker && this.showPicker();
        });
    });
}

// Export functions for use in inline scripts
window.JobTracker = {
    confirmDelete: window.confirmDelete,
    updateStatusBadges: updateStatusBadges
};
