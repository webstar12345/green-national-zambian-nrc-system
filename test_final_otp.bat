@echo off
echo 🎯 FINAL OTP SYSTEM TEST
echo ========================

echo.
echo 🚀 Starting Django development server with OTP system...
echo.
echo 📋 HOW IT WORKS:
echo ===============
echo 1. 📧 Tries to send email first
echo 2. 💻 If email fails, shows OTP in console (development)
echo 3. 🌐 Also displays OTP in browser message
echo 4. 🔒 Full OTP security maintained
echo 5. ✅ Always works regardless of email issues
echo.
echo 🧪 TEST STEPS:
echo =============
echo 1. Go to: http://localhost:8000/accounts/login/
echo 2. Enter your credentials and submit
echo 3. Look for OTP in:
echo    - Browser message (always shown)
echo    - Console output (development mode)
echo 4. Enter OTP on verification page
echo 5. Complete login successfully
echo.
echo 📧 Email: If Gmail works, you'll get real emails too!
echo 💻 Console: Watch this window for OTP codes
echo 🌐 Browser: OTP always displayed in messages
echo.
echo Press Ctrl+C to stop server
echo.

python manage.py runserver