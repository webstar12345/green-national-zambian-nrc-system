/**
 * Dark Mode Toggle for NRC System
 * Persists user preference in localStorage
 */

(function() {
    'use strict';
    
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply theme on page load
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        // Create dark mode toggle button
        createDarkModeToggle();
        
        // Update toggle button icon
        updateToggleIcon();
    });
    
    function createDarkModeToggle() {
        // Check if toggle already exists
        if (document.getElementById('darkModeToggle')) {
            return;
        }
        
        // Create toggle button
        const toggle = document.createElement('button');
        toggle.id = 'darkModeToggle';
        toggle.className = 'dark-mode-toggle';
        toggle.setAttribute('aria-label', 'Toggle dark mode');
        toggle.innerHTML = '<i class="fas fa-moon"></i>';
        
        // Add click event
        toggle.addEventListener('click', toggleDarkMode);
        
        // Add to body
        document.body.appendChild(toggle);
    }
    
    function toggleDarkMode() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Apply new theme
        document.documentElement.setAttribute('data-theme', newTheme);
        
        // Save preference
        localStorage.setItem('theme', newTheme);
        
        // Update icon
        updateToggleIcon();
        
        // Dispatch custom event for other components
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: newTheme } }));
    }
    
    function updateToggleIcon() {
        const toggle = document.getElementById('darkModeToggle');
        if (!toggle) return;
        
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const icon = toggle.querySelector('i');
        
        if (currentTheme === 'dark') {
            icon.className = 'fas fa-sun';
            toggle.setAttribute('aria-label', 'Switch to light mode');
        } else {
            icon.className = 'fas fa-moon';
            toggle.setAttribute('aria-label', 'Switch to dark mode');
        }
    }
    
    // Export functions for external use
    window.darkMode = {
        toggle: toggleDarkMode,
        getCurrentTheme: function() {
            return document.documentElement.getAttribute('data-theme');
        },
        setTheme: function(theme) {
            if (theme === 'dark' || theme === 'light') {
                document.documentElement.setAttribute('data-theme', theme);
                localStorage.setItem('theme', theme);
                updateToggleIcon();
            }
        }
    };
})();
