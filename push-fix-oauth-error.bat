@echo off
echo ========================================
echo Fixing OAuth Template Error
echo ========================================
echo.
echo Removing Google OAuth sections from templates...
echo.

git add templates/accounts/login.html
git add templates/accounts/signup.html
git commit -m "Fix: Remove Google OAuth from templates (not configured)"
git push origin main

echo.
echo ========================================
echo Fix Deployed!
echo ========================================
echo.
echo The OAuth error should be resolved.
echo Wait 2-3 minutes for Render to rebuild.
echo.
pause
