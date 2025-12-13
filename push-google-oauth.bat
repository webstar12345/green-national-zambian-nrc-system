@echo off
echo ========================================
echo Deploying Google OAuth Login
echo ========================================
echo.

git add requirements.txt
git add nrc_system/settings.py
git add nrc_system/urls.py
git add templates/accounts/login.html
git add templates/accounts/signup.html
git add accounts/management/commands/setup_google_oauth.py
git add GOOGLE_OAUTH_SETUP.md
git add .env.example
git commit -m "Add Google OAuth login functionality"
git push origin main

echo.
echo ========================================
echo Google OAuth Code Deployed!
echo ========================================
echo.
echo IMPORTANT: After deployment completes:
echo 1. Set up Google Cloud Console (see GOOGLE_OAUTH_SETUP.md)
echo 2. Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to Render environment
echo 3. Run: python manage.py setup_google_oauth
echo 4. Test login at your site
echo.
pause
