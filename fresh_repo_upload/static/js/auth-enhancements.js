/**
 * Authentication Enhancements
 * - Password visibility toggle
 * - Button loading states
 * - Page loader
 */

// Page Loader
document.addEventListener('DOMContentLoaded', function() {
    // Hide page loader when page is fully loaded
    const pageLoader = document.getElementById('pageLoader');
    if (pageLoader) {
        setTimeout(() => {
            pageLoader.classList.add('hidden');
            document.body.classList.remove('loading');
        }, 500);
    }
});

// Password Toggle Functionality
function initPasswordToggles() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(field => {
        // Skip if already wrapped
        if (field.parentElement.classList.contains('password-field-wrapper')) {
            return;
        }
        
        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'password-field-wrapper';
        
        // Wrap the input
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);
        
        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'password-toggle';
        toggleBtn.setAttribute('aria-label', 'Toggle password visibility');
        toggleBtn.innerHTML = '<i class="fas fa-eye"></i>';
        
        // Add toggle button after input
        wrapper.appendChild(toggleBtn);
        
        // Toggle functionality
        toggleBtn.addEventListener('click', function() {
            const type = field.getAttribute('type');
            const icon = this.querySelector('i');
            
            if (type === 'password') {
                field.setAttribute('type', 'text');
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
                this.setAttribute('aria-label', 'Hide password');
            } else {
                field.setAttribute('type', 'password');
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
                this.setAttribute('aria-label', 'Show password');
            }
        });
    });
}

// Button Loading State
function addButtonLoader(button) {
    if (button.classList.contains('btn-loading')) {
        return;
    }
    
    button.classList.add('btn-loading');
    
    // Wrap button text
    const buttonText = button.innerHTML;
    button.innerHTML = `<span class="btn-text">${buttonText}</span><div class="btn-loader"></div>`;
}

function removeButtonLoader(button) {
    button.classList.remove('btn-loading');
    const textSpan = button.querySelector('.btn-text');
    if (textSpan) {
        button.innerHTML = textSpan.innerHTML;
    }
}

// Form Submit Handler with Loading
function initFormLoaders() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            
            if (submitBtn && !submitBtn.classList.contains('btn-loading')) {
                addButtonLoader(submitBtn);
                
                // If form validation fails, remove loader
                setTimeout(() => {
                    if (!this.checkValidity()) {
                        removeButtonLoader(submitBtn);
                    }
                }, 100);
            }
        });
    });
}

// Initialize all enhancements
document.addEventListener('DOMContentLoaded', function() {
    initPasswordToggles();
    initFormLoaders();
});

// Re-initialize on dynamic content load (for AJAX forms)
if (typeof window.reinitAuthEnhancements === 'undefined') {
    window.reinitAuthEnhancements = function() {
        initPasswordToggles();
        initFormLoaders();
    };
}
