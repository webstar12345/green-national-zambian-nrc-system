@echo off
echo Pushing ALLOWED_HOSTS fix to GitHub...
git add nrc_system/settings.py
git commit -m "Fix: Add RENDER_EXTERNAL_HOSTNAME to ALLOWED_HOSTS"
git push
echo.
echo Done! Now add RENDER_EXTERNAL_HOSTNAME to Render environment variables.
pause
