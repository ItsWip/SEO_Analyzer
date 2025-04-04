/**
 * Main JavaScript file for SEO Analyzer
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // URL input validation
    const urlInput = document.getElementById('url');
    if (urlInput) {
        urlInput.addEventListener('input', function(e) {
            let url = e.target.value.trim();
            
            // Add https:// if no protocol is specified
            if (url && url.length > 0 && !url.match(/^https?:\/\//i)) {
                // Don't add protocol while user is still typing
                if (url.includes('.') && !url.endsWith('.')) {
                    e.target.classList.add('is-valid');
                }
            }
        });
    }
    
    // Show loading indicator on form submission
    const analysisForm = document.querySelector('form');
    if (analysisForm) {
        analysisForm.addEventListener('submit', function(e) {
            if (this.checkValidity()) {
                // Create and show loading overlay
                const loadingOverlay = document.createElement('div');
                loadingOverlay.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center';
                loadingOverlay.style.backgroundColor = 'rgba(0,0,0,0.7)';
                loadingOverlay.style.zIndex = '9999';
                
                const spinner = document.createElement('div');
                spinner.className = 'spinner-border text-light';
                spinner.setAttribute('role', 'status');
                spinner.style.width = '3rem';
                spinner.style.height = '3rem';
                
                const loadingText = document.createElement('div');
                loadingText.className = 'text-light mt-3';
                loadingText.textContent = 'Analyzing website... This may take a moment.';
                
                const spinnerContainer = document.createElement('div');
                spinnerContainer.className = 'd-flex flex-column align-items-center';
                spinnerContainer.appendChild(spinner);
                spinnerContainer.appendChild(loadingText);
                
                loadingOverlay.appendChild(spinnerContainer);
                document.body.appendChild(loadingOverlay);
            }
        });
    }
    
    // Expandable sections
    const expandButtons = document.querySelectorAll('.expand-btn');
    expandButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.classList.toggle('d-none');
                
                // Toggle button text
                if (this.innerHTML.includes('Show more')) {
                    this.innerHTML = this.innerHTML.replace('Show more', 'Show less');
                    this.innerHTML = this.innerHTML.replace('fa-chevron-down', 'fa-chevron-up');
                } else {
                    this.innerHTML = this.innerHTML.replace('Show less', 'Show more');
                    this.innerHTML = this.innerHTML.replace('fa-chevron-up', 'fa-chevron-down');
                }
            }
        });
    });
});

/**
 * Updates the circular progress bars
 * @param {HTMLElement} element - The progress bar element
 * @param {number} value - The progress value (0-100)
 */
function updateCircularProgress(element, value) {
    if (!element) return;
    
    // Calculate color based on value
    let color;
    if (value >= 80) {
        color = 'var(--bs-success)';
    } else if (value >= 50) {
        color = 'var(--bs-warning)';
    } else {
        color = 'var(--bs-danger)';
    }
    
    // Update the gradient
    element.style.background = `conic-gradient(
        ${color} ${value}%, 
        var(--bs-dark) ${value}%
    )`;
}
