@echo off
echo ========================================
echo Deploying OAuth Fix to Production
echo ========================================

git add .
git commit -m "Fix: Update OAuth configuration for new Google credentials"
git push origin main

echo.
echo ========================================
echo Deployment pushed to GitHub!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Go to Render Dashboard
echo 2. Update environment variables:
echo    - GOOGLE_CLIENT_ID
echo    - GOOGLE_CLIENT_SECRET
echo 3. Wait for auto-deploy to complete
echo 4. Run Django admin commands on Render
echo ========================================
pause
