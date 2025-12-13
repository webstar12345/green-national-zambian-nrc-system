@echo off
echo 🔧 Fixing OTP Email System...
echo.

echo 📧 Current Email Configuration:
echo EMAIL_HOST_USER: simoongalaurent427@gmail.com
echo EMAIL_HOST: smtp.gmail.com
echo EMAIL_PORT: 587
echo.

echo 🚀 Deploying OTP Email Fix...

git add accounts/otp_service.py
git add nrc_system/settings.py
git add templates/accounts/otp_email.html
git add FIX_OTP_EMAIL_ISSUE.md
git add diagnose_email_config.py
git add test_otp_local.py
git add fix_otp_email_now.bat

git commit -m "Fix OTP email system - Update SMTP configuration and diagnostics"

git push origin main

echo.
echo ✅ Code deployed! Now update Render environment variables:
echo 1. Go to Render Dashboard: https://dashboard.render.com/
echo 2. Select your service: green-national-zambian-nrc-system
echo 3. Go to Environment tab
echo 4. Add/Update these variables:
echo    EMAIL_HOST=smtp.gmail.com
echo    EMAIL_PORT=587
echo    EMAIL_USE_TLS=True
echo    EMAIL_HOST_USER=simoongalaurent427@gmail.com
echo    EMAIL_HOST_PASSWORD=bqhtkqaslcixwsjg
echo    DEFAULT_FROM_EMAIL=simoongalaurent427@gmail.com
echo    DEBUG=False
echo.
echo 🧪 After updating Render variables, test OTP at:
echo https://green-national-zambian-nrc-system.onrender.com
echo.
pause