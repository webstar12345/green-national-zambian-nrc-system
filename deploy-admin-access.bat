@echo off
echo ========================================
echo Deploying Admin Access Setup
echo ========================================
echo.
echo This will push the admin creation command to production.
echo.
echo IMPORTANT: After deployment, you need to:
echo 1. Add these environment variables on Render:
echo    - ADMIN_USERNAME=your_username
echo    - ADMIN_EMAIL=your_email@example.com
echo    - ADMIN_PASSWORD=your_secure_password
echo.
echo 2. Run this command in Render Shell:
echo    python manage.py createdefaultadmin
echo.
echo ========================================
pause

git add .
git commit -m "Add admin credential checker and OAuth fix"
git push origin main

echo.
echo ========================================
echo Pushed to GitHub!
echo ========================================
echo.
echo NEXT STEPS ON RENDER:
echo.
echo 1. Go to Render Dashboard
echo 2. Add Environment Variables:
echo    ADMIN_USERNAME = your_admin_username
echo    ADMIN_EMAIL = your_email@example.com
echo    ADMIN_PASSWORD = YourSecurePassword123!
echo    GOOGLE_CLIENT_ID = your_new_client_id
echo    GOOGLE_CLIENT_SECRET = your_new_client_secret
echo.
echo 3. Wait for auto-deploy to complete
echo.
echo 4. Open Shell tab and run:
echo    python manage.py createdefaultadmin
echo.
echo 5. Login at: https://green-national-zambian-nrc-system.onrender.com/admin/
echo.
echo ========================================
pause
