@echo off
echo ========================================
echo Deploying iOS PWA Support
echo ========================================
echo.
echo New Features:
echo - iOS-specific icons (120, 152, 167, 180)
echo - iOS meta tags and configuration
echo - Custom iOS install prompt
echo - iOS splash screen support
echo - Safari-optimized PWA
echo.

git add static/images/icons/*.png
git add static/js/ios-install-prompt.js
git add static/css/ios-install-prompt.css
git add static/manifest.json
git add templates/base.html
git add generate_pwa_icons.py
git add IOS_INSTALLATION_GUIDE.md
git add push-ios-support.bat
git commit -m "Add complete iOS PWA support for iPhone and iPad"
git push origin main

echo.
echo ========================================
echo iOS Support Deployed!
echo ========================================
echo.
echo Your app is now installable on:
echo ✓ iPhone (iOS 11.3+)
echo ✓ iPad (iOS 11.3+)
echo ✓ Android devices
echo ✓ Windows desktops
echo.
echo Installation:
echo - iOS: Safari → Share → Add to Home Screen
echo - Android: Chrome → Install prompt
echo - Desktop: Chrome → Install button
echo.
echo Wait 2-3 minutes for Render to rebuild.
echo.
pause
