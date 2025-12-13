@echo off
echo ========================================
echo  DATABASE RESET OPTION - Last Resort
echo ========================================
echo.

echo If the cache fix doesn't work, this is the nuclear option:
echo Reset the entire database to clear all migration issues
echo.

echo STEPS TO RESET DATABASE ON RENDER:
echo.
echo 1. Go to your Render Dashboard
echo 2. Find your PostgreSQL database service
echo 3. Go to "Settings" tab
echo 4. Scroll down to "Danger Zone"
echo 5. Click "Reset Database"
echo 6. Confirm the reset
echo.
echo 7. After reset, redeploy your service:
echo    - Go to your web service
echo    - Click "Manual Deploy"
echo    - Select "Deploy latest commit"
echo.
echo WARNING: This will delete all existing data!
echo But it will guarantee a clean deployment.
echo.
echo ALTERNATIVE: Create new database:
echo 1. Create new PostgreSQL database on Render
echo 2. Update DATABASE_URL environment variable
echo 3. Redeploy service
echo.
echo This completely bypasses all migration cache issues.
echo.
pause