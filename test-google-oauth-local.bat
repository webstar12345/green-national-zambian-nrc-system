@echo off
echo ========================================
echo Testing Google OAuth Locally
echo ========================================
echo.

echo Checking if django-allauth is installed...
python -c "import allauth" 2>nul
if errorlevel 1 (
    echo Installing django-allauth...
    pip install django-allauth==0.57.0
) else (
    echo ✓ django-allauth is installed
)

echo.
echo Running migrations...
python manage.py migrate

echo.
echo Checking for errors...
python manage.py check

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To test locally:
echo 1. Make sure you have GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env
echo 2. Run: python manage.py runserver
echo 3. Visit: http://localhost:8000/accounts/login/
echo 4. You should see "Sign in with Google" button
echo.
echo Note: For local testing, add this redirect URI to Google Console:
echo http://localhost:8000/accounts/google/login/callback/
echo.
pause
