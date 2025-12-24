@echo off
echo 📧 SETTING UP REAL OTP EMAILS
echo =============================

echo.
echo 🔧 Step 1: Forcing Gmail configuration in Django...
python force_gmail_in_django.py

echo.
echo 🧪 Step 2: Testing Gmail connection...
python verify_gmail_password.py

echo.
echo 🚀 Step 3: Starting Django server with real email support...
echo.
echo 📋 WHAT TO EXPECT:
echo ==================
echo ✅ Real OTP emails sent to: simoongalaurent427@gmail.com
echo ✅ Professional email template with NRC branding
echo ✅ 6-digit OTP codes that work for login
echo ✅ No more fallback messages - real emails only!
echo.
echo 🧪 TEST STEPS:
echo =============
echo 1. Go to: http://localhost:8000/accounts/login/
echo 2. Enter your credentials and submit
echo 3. Check your Gmail: simoongalaurent427@gmail.com
echo 4. Look for "NRC Zambia - Verification Code" email
echo 5. Enter the OTP from email on verification page
echo 6. Complete login successfully
echo.
echo 📧 Gmail Details:
echo   Email: simoongalaurent427@gmail.com
echo   App Password: sghuygvzhowzrdmm
echo   SMTP: smtp.gmail.com:587
echo.
echo Press Ctrl+C to stop server
echo.

python manage.py runserver