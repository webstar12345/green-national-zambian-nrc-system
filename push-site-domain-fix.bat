@echo off
echo ========================================
echo  Deploying Site Domain Auto-Update Fix
echo ========================================
echo.

echo Adding files to git...
git add accounts/management/commands/update_site_domain.py
git add build.sh

echo.
echo Committing changes...
git commit -m "Add automatic site domain update for production Google OAuth"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo  Deployment Complete!
echo ========================================
echo.
echo The site domain will now automatically update on Render deployment.
echo After deployment completes, Google OAuth should work!
echo.
pause
