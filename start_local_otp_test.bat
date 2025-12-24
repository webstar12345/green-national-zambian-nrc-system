@echo off
echo 🏠 STARTING LOCAL OTP EMAIL TEST
echo ================================

echo.
echo 📧 Testing Gmail SMTP configuration...
python test_local_otp_email.py

echo.
echo 🚀 Starting Django development server...
echo.
echo 🎯 NEXT STEPS:
echo 1. Server will start on http://localhost:8000
echo 2. Go to http://localhost:8000/accounts/login/
echo 3. Try to login with your credentials
echo 4. Check your email for OTP code
echo 5. Enter OTP to complete login
echo.
echo 📧 OTP emails should arrive at: simoongalaurent427@gmail.com
echo 🔑 Using Gmail app password: sghuygvzhowzrdmm
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver