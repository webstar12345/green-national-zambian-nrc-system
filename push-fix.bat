@echo off
echo Pushing fixes to GitHub...
git add requirements.txt
git add setup.py
git commit -m "Fix: Update Pillow version and remove setup.py for Render deployment"
git push
echo.
echo Done! Render will automatically redeploy with the fixes.
pause
