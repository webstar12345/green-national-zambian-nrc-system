@echo off
echo 🔧 Fixing OTP Email Issue for Production
echo ========================================

echo.
echo 📧 Step 1: Updating email configuration...
git add .env
git add FIX_OTP_EMAIL_ISSUE.md
git add fix_otp_email_production.bat

echo.
echo 📝 Step 2: Committing email fixes...
git commit -m "Fix OTP email configuration for production

- Updated .env with proper Gmail SMTP settings
- Added comprehensive email setup guide
- Fixed DEFAULT_FROM_EMAIL to use actual Gmail address
- Added troubleshooting documentation

IMPORTANT: Update EMAIL_HOST_PASSWORD on Render with Gmail app password"

echo.
echo 🚀 Step 3: Deploying to production...
git push origin main

echo.
echo ✅ Deployment complete!
echo.
echo 🔔 IMPORTANT NEXT STEPS:
echo 1. Get Gmail App Password from: https://myaccount.google.com/security
echo 2. Go to Render Dashboard → Environment Variables
echo 3. Update EMAIL_HOST_PASSWORD with your 16-character app password
echo 4. Test OTP functionality on live site
echo.
echo 📖 See FIX_OTP_EMAIL_ISSUE.md for detailed instructions
pause