/**
 * iOS Installation Prompt
 * Shows custom install instructions for iOS devices
 */

(function() {
    'use strict';
    
    // Check if device is iOS
    function isIOS() {
        return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    }
    
    // Check if already installed (standalone mode)
    function isInstalled() {
        return window.navigator.standalone === true || 
               window.matchMedia('(display-mode: standalone)').matches;
    }
    
    // Check if user has dismissed the prompt before
    function hasBeenDismissed() {
        return localStorage.getItem('iosInstallPromptDismissed') === 'true';
    }
    
    // Show iOS install prompt
    function showIOSInstallPrompt() {
        // Don't show if already installed or dismissed
        if (isInstalled() || hasBeenDismissed()) {
            return;
        }
        
        // Create prompt HTML
        const promptHTML = `
            <div class="ios-install-prompt" id="iosInstallPrompt">
                <div class="ios-install-content">
                    <button class="ios-install-close" id="iosInstallClose">
                        <i class="fas fa-times"></i>
                    </button>
                    <div class="ios-install-icon">
                        <i class="fas fa-mobile-alt"></i>
                    </div>
                    <h3>Install NRC Zambia App</h3>
                    <p>Add this app to your home screen for quick access!</p>
                    <div class="ios-install-steps">
                        <div class="ios-step">
                            <span class="ios-step-number">1</span>
                            <p>Tap the <i class="fas fa-share"></i> Share button below</p>
                        </div>
                        <div class="ios-step">
                            <span class="ios-step-number">2</span>
                            <p>Scroll and tap <strong>"Add to Home Screen"</strong></p>
                        </div>
                        <div class="ios-step">
                            <span class="ios-step-number">3</span>
                            <p>Tap <strong>"Add"</strong> in the top right</p>
                        </div>
                    </div>
                    <button class="ios-install-dismiss" id="iosInstallDismiss">
                        Got it!
                    </button>
                </div>
            </div>
        `;
        
        // Add to page
        document.body.insertAdjacentHTML('beforeend', promptHTML);
        
        // Add event listeners
        document.getElementById('iosInstallClose').addEventListener('click', dismissPrompt);
        document.getElementById('iosInstallDismiss').addEventListener('click', dismissPrompt);
        
        // Show with animation
        setTimeout(() => {
            document.getElementById('iosInstallPrompt').classList.add('show');
        }, 100);
    }
    
    function dismissPrompt() {
        const prompt = document.getElementById('iosInstallPrompt');
        if (prompt) {
            prompt.classList.remove('show');
            setTimeout(() => {
                prompt.remove();
            }, 300);
        }
        
        // Remember dismissal
        localStorage.setItem('iosInstallPromptDismissed', 'true');
    }
    
    // Initialize
    if (isIOS()) {
        // Show prompt after 3 seconds
        setTimeout(showIOSInstallPrompt, 3000);
    }
})();
