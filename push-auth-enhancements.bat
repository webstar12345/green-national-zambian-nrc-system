@echo off
echo ========================================
echo Deploying Auth Enhancements
echo ========================================
echo.
echo Features:
echo - Password visibility toggle (eye icon)
echo - Button loading states
echo - Page loader on app startup
echo.

git add static/css/auth-enhancements.css
git add static/js/auth-enhancements.js
git add templates/base.html
git add templates/accounts/login.html
git add templates/accounts/signup.html
git commit -m "Add password toggle, button loaders, and page loader"
git push origin main

echo.
echo ========================================
echo Auth Enhancements Deployed!
echo ========================================
echo.
echo Changes:
echo ✓ Password fields now have eye icon to show/hide
echo ✓ Login and Register buttons show loading spinner
echo ✓ Page loader displays when app opens
echo.
echo Wait 2-3 minutes for Render to rebuild.
echo.
pause
