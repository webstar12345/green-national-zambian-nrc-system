@echo off
echo ========================================
echo Deploying PWA Icons to Render
echo ========================================
echo.

git add static/images/icons/*.png
git add generate_pwa_icons.py
git commit -m "Add PWA icons for installable app"
git push origin main

echo.
echo ========================================
echo PWA Icons Deployed Successfully!
echo ========================================
echo.
echo Your PWA should now be installable with proper icons.
echo Wait 2-3 minutes for Render to rebuild.
echo.
pause
