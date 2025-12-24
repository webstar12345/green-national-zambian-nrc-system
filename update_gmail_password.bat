@echo off
echo 🔑 GMAIL APP PASSWORD UPDATE
echo ===========================

echo.
echo 📋 STEPS TO GET NEW APP PASSWORD:
echo 1. Go to: https://myaccount.google.com/security
echo 2. Click "App passwords" 
echo 3. Select "Mail" and "Other (custom name)"
echo 4. Enter "NRC System OTP" as name
echo 5. Copy the 16-character password
echo.

set /p newpassword="Enter your new Gmail app password: "

echo.
echo 🔄 Updating .env file...

powershell -Command "(Get-Content .env) -replace 'EMAIL_HOST_PASSWORD=.*', 'EMAIL_HOST_PASSWORD=%newpassword%' | Set-Content .env"

echo ✅ Updated .env file with new password: %newpassword%
echo.
echo 🧪 Testing new password...
python verify_gmail_password.py

echo.
echo 🎯 If test passes, your OTP emails will work!
pause