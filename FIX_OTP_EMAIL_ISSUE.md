# 🔧 Fix OTP Email Issue - Complete Guide

## 📧 Problem
Users can't receive OTP emails because Gmail SMTP is not properly configured in production.

## 🎯 Solution Steps

### Step 1: Get Gmail App Password
1. Go to your Google Account settings: https://myaccount.google.com/
2. Click "Security" → "2-Step Verification" (enable if not already)
3. Click "App passwords" 
4. Generate a new app password for "Mail"
5. Copy the 16-character password (like: `abcd efgh ijkl mnop`)

### Step 2: Update Environment Variables on Render
1. Go to your Render dashboard
2. Select your service: `green-national-zambian-nrc-system`
3. Go to "Environment" tab
4. Add/Update these variables:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=simoongalaurent427@gmail.com
EMAIL_HOST_PASSWORD=YOUR_16_CHAR_APP_PASSWORD_HERE
DEFAULT_FROM_EMAIL=simoongalaurent427@gmail.com
DEBUG=False
```

### Step 3: Deploy the Fix
Run the deployment script to apply changes:

```bash
./fix_otp_email_production.bat
```

## 🧪 Testing
After deployment, test OTP functionality:
1. Visit your live site
2. Try to register/login
3. Check if OTP email arrives
4. Verify OTP works correctly

## 🔍 Troubleshooting

### If emails still don't work:
1. **Check Gmail Security**: Ensure 2FA is enabled
2. **Verify App Password**: Make sure it's correct (no spaces)
3. **Check Spam Folder**: OTP emails might go to spam
4. **Try Different Email**: Test with different email providers

### Alternative Email Providers:
If Gmail doesn't work, try:
- **SendGrid** (recommended for production)
- **Mailgun**
- **Amazon SES**

## 📋 Current Status
- ✅ OTP system code is working correctly
- ✅ Email templates are properly formatted
- ❌ SMTP configuration needs Gmail app password
- ❌ Production environment variables need updating

## 🚀 Next Steps
1. Get Gmail app password
2. Update Render environment variables
3. Deploy changes
4. Test OTP functionality