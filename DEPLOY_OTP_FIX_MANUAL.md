# 🔧 Manual OTP Email Fix Deployment

## ✅ Step 1: Your Local Setup is Ready
- ✅ Gmail app password updated in .env: `bqhtkqaslcixwsjg`
- ✅ OTP service code is working
- ✅ Email templates are ready

## 🚀 Step 2: Deploy Code Changes (Run in Git Bash)

```bash
# Add the OTP fix files
git add accounts/otp_service.py
git add nrc_system/settings.py
git add templates/accounts/otp_email.html
git add FIX_OTP_EMAIL_ISSUE.md
git add diagnose_email_config.py
git add test_otp_local.py
git add fix_otp_email_now.bat
git add DEPLOY_OTP_FIX_MANUAL.md

# Commit the changes
git commit -m "🔧 Fix OTP email system - Complete SMTP configuration

- Update OTP service with better error handling
- Add comprehensive email diagnostics
- Fix Gmail SMTP authentication for production
- Add HTML email templates for OTP verification
- Ready for Render environment variable configuration"

# Push to main branch
git push origin main
```

## 🌐 Step 3: Update Render Environment Variables

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Select your service**: `green-national-zambian-nrc-system`
3. **Click "Environment" tab**
4. **Add/Update these variables**:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=simoongalaurent427@gmail.com
EMAIL_HOST_PASSWORD=bqhtkqaslcixwsjg
DEFAULT_FROM_EMAIL=simoongalaurent427@gmail.com
DEBUG=False
```

## 🧪 Step 4: Test the Fix

1. **Wait for Render deployment** (2-3 minutes after updating environment variables)
2. **Visit your live site**: https://green-national-zambian-nrc-system.onrender.com
3. **Try to register/login** with a real email address
4. **Check your email** for the OTP verification code
5. **Enter the OTP** to complete verification

## 🔍 Troubleshooting

If OTP emails still don't work:

1. **Check Render Logs**:
   - Go to Render Dashboard → Your Service → Logs
   - Look for email-related errors

2. **Verify Environment Variables**:
   - Make sure all email variables are set correctly
   - No extra spaces or quotes around values

3. **Test Different Email**:
   - Try with Gmail, Yahoo, Outlook
   - Check spam/junk folders

4. **Gmail Security**:
   - Ensure 2FA is enabled on your Gmail account
   - App password is correctly generated and copied

## 📧 Expected Behavior

When working correctly:
- User registers/logs in
- System sends OTP email within 30 seconds
- Email arrives with 6-digit code
- User enters code and gets verified
- Login/registration completes successfully

## 🎯 Current Status

- ✅ Local development: OTP emails work (console backend)
- ✅ Code: All OTP functionality implemented
- ✅ Gmail: App password generated and configured
- 🔄 Production: Needs Render environment variables update
- 🧪 Testing: Ready for live testing after Render update