// PWA Installation Handler
let deferredPrompt;
let installButton;

// Register service worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/sw.js')
      .then((registration) => {
        console.log('ServiceWorker registered:', registration.scope);
      })
      .catch((error) => {
        console.log('ServiceWorker registration failed:', error);
      });
  });
}

// Create install button
function createInstallButton() {
  const installPrompt = document.createElement('div');
  installPrompt.id = 'pwa-install-prompt';
  installPrompt.className = 'pwa-install-prompt';
  installPrompt.innerHTML = `
    <div class="pwa-install-content">
      <div class="pwa-install-icon">
        <i class="fas fa-mobile-alt"></i>
      </div>
      <div class="pwa-install-text">
        <h3>Install NRC App</h3>
        <p>Add to your home screen for quick access</p>
      </div>
      <div class="pwa-install-actions">
        <button id="pwa-install-btn" class="pwa-btn-install">
          <i class="fas fa-download"></i> Install
        </button>
        <button id="pwa-dismiss-btn" class="pwa-btn-dismiss">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(installPrompt);
  
  installButton = document.getElementById('pwa-install-btn');
  const dismissButton = document.getElementById('pwa-dismiss-btn');
  
  installButton.addEventListener('click', installApp);
  dismissButton.addEventListener('click', dismissPrompt);
}

// Listen for beforeinstallprompt event
window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent the mini-infobar from appearing on mobile
  e.preventDefault();
  
  // Stash the event so it can be triggered later
  deferredPrompt = e;
  
  // Check if user has dismissed before
  const dismissed = localStorage.getItem('pwa-install-dismissed');
  const dismissedTime = localStorage.getItem('pwa-install-dismissed-time');
  
  // Show prompt if not dismissed or dismissed more than 7 days ago
  if (!dismissed || (Date.now() - dismissedTime > 7 * 24 * 60 * 60 * 1000)) {
    // Show install prompt after 5 seconds
    setTimeout(() => {
      createInstallButton();
      showInstallPrompt();
    }, 5000);
  }
});

function showInstallPrompt() {
  const prompt = document.getElementById('pwa-install-prompt');
  if (prompt) {
    prompt.classList.add('show');
  }
}

function hideInstallPrompt() {
  const prompt = document.getElementById('pwa-install-prompt');
  if (prompt) {
    prompt.classList.remove('show');
    setTimeout(() => {
      prompt.remove();
    }, 300);
  }
}

async function installApp() {
  if (!deferredPrompt) {
    return;
  }
  
  // Show the install prompt
  deferredPrompt.prompt();
  
  // Wait for the user to respond to the prompt
  const { outcome } = await deferredPrompt.userChoice;
  
  console.log(`User response to the install prompt: ${outcome}`);
  
  if (outcome === 'accepted') {
    console.log('User accepted the install prompt');
    // Track installation
    trackInstallation('accepted');
  } else {
    console.log('User dismissed the install prompt');
    trackInstallation('dismissed');
  }
  
  // Clear the deferredPrompt
  deferredPrompt = null;
  
  // Hide the install prompt
  hideInstallPrompt();
}

function dismissPrompt() {
  // Store dismissal in localStorage
  localStorage.setItem('pwa-install-dismissed', 'true');
  localStorage.setItem('pwa-install-dismissed-time', Date.now());
  
  hideInstallPrompt();
  
  // Track dismissal
  trackInstallation('dismissed-by-user');
}

function trackInstallation(action) {
  // Track installation analytics
  console.log('PWA Installation:', action);
  
  // You can send this to your analytics service
  // Example: gtag('event', 'pwa_install', { action: action });
}

// Detect if app is installed
window.addEventListener('appinstalled', (evt) => {
  console.log('PWA was installed');
  hideInstallPrompt();
  
  // Show thank you message
  showThankYouMessage();
  
  // Track successful installation
  trackInstallation('installed');
});

function showThankYouMessage() {
  const message = document.createElement('div');
  message.className = 'pwa-thank-you';
  message.innerHTML = `
    <div class="pwa-thank-you-content">
      <i class="fas fa-check-circle"></i>
      <h3>App Installed!</h3>
      <p>You can now access NRC System from your home screen</p>
    </div>
  `;
  
  document.body.appendChild(message);
  
  setTimeout(() => {
    message.classList.add('show');
  }, 100);
  
  setTimeout(() => {
    message.classList.remove('show');
    setTimeout(() => {
      message.remove();
    }, 300);
  }, 5000);
}

// Check if running as PWA
function isPWA() {
  return window.matchMedia('(display-mode: standalone)').matches ||
         window.navigator.standalone === true;
}

// Add PWA class to body if running as app
if (isPWA()) {
  document.body.classList.add('pwa-mode');
  console.log('Running as PWA');
}

// iOS Add to Home Screen detection
function isIOS() {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
}

function isInStandaloneMode() {
  return ('standalone' in window.navigator) && (window.navigator.standalone);
}

// Show iOS install instructions
if (isIOS() && !isInStandaloneMode()) {
  setTimeout(() => {
    showIOSInstructions();
  }, 10000);
}

function showIOSInstructions() {
  const dismissed = localStorage.getItem('ios-install-dismissed');
  if (dismissed) return;
  
  const iosPrompt = document.createElement('div');
  iosPrompt.className = 'ios-install-prompt';
  iosPrompt.innerHTML = `
    <div class="ios-install-content">
      <button class="ios-close-btn" onclick="this.parentElement.parentElement.remove(); localStorage.setItem('ios-install-dismissed', 'true');">
        <i class="fas fa-times"></i>
      </button>
      <h3>Install NRC App</h3>
      <p>Tap <i class="fas fa-share"></i> then "Add to Home Screen"</p>
      <div class="ios-steps">
        <div class="ios-step">
          <span class="step-number">1</span>
          <p>Tap the share button</p>
        </div>
        <div class="ios-step">
          <span class="step-number">2</span>
          <p>Scroll and tap "Add to Home Screen"</p>
        </div>
        <div class="ios-step">
          <span class="step-number">3</span>
          <p>Tap "Add" to install</p>
        </div>
      </div>
    </div>
  `;
  
  document.body.appendChild(iosPrompt);
  
  setTimeout(() => {
    iosPrompt.classList.add('show');
  }, 100);
}

// Update available notification
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    showUpdateNotification();
  });
}

function showUpdateNotification() {
  const notification = document.createElement('div');
  notification.className = 'pwa-update-notification';
  notification.innerHTML = `
    <div class="pwa-update-content">
      <i class="fas fa-sync-alt"></i>
      <p>New version available!</p>
      <button onclick="window.location.reload()">Update Now</button>
    </div>
  `;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.classList.add('show');
  }, 100);
}
