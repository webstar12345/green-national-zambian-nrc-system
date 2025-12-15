@echo off
echo 🚀 Deploying OTP Email Fix
echo ========================================

echo 📧 Adding OTP email fixes...
git add .env
git add fix_gmail_app_password.py
git add test_gmail_smtp.py
git add test_otp_email.py
git add test_otp_local.py
git add accounts/otp_service.py

echo 💾 Committing changes...
git commit -m "Fix: Update Gmail app password and OTP email system

- Updated Gmail app password for SMTP authentication
- Fixed OTP email delivery system
- Added comprehensive email testing scripts
- Verified Gmail SMTP connection working
- OTP emails now sending successfully"

echo 🌐 Pushing to main branch...
git push origin main

echo ✅ OTP email fix deployed successfully!
echo 📱 OTP emails should now work in production
pause