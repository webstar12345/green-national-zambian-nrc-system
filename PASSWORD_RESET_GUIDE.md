# Password Reset Feature Guide

## Overview
Complete password reset functionality has been implemented for the Zambian NRC System, allowing users to reset their passwords via email.

## Features Implemented

### 1. Forgot Password Link
- Added "Forgot your password?" link on the login page
- Located below the password field
- Links to password reset form

### 2. Password Reset Flow
1. **Request Reset** - User enters email address
2. **Email Sent** - Confirmation page shown
3. **Email Received** - User gets reset link via email
4. **Set New Password** - User enters new password twice
5. **Success** - Confirmation and redirect to login

### 3. Security Features
- ✅ Reset links expire after 24 hours
- ✅ One-time use tokens
- ✅ Secure password validation
- ✅ Email verification required
- ✅ Invalid link detection

## How to Use (User Perspective)

### Step 1: Request Password Reset
1. Go to login page
2. Click "Forgot your password?"
3. Enter your email address
4. Click "Send Reset Instructions"

### Step 2: Check Email
1. Check your email inbox
2. Look for email from Zambian NRC System
3. Click the reset link in the email
4. (Link expires in 24 hours)

### Step 3: Set New Password
1. Enter your new password
2. Confirm the new password
3. Click "Reset Password"

### Step 4: Login
1. You'll see a success message
2. Click "Login with New Password"
3. Use your new password to login

## Email Configuration

### Development Mode (Current Setup)
- Emails are printed to the console
- No actual emails are sent
- Perfect for testing

**To see the reset email:**
1. Request password reset
2. Check your terminal/console
3. Copy the reset link from the console output
4. Paste it in your browser

### Production Mode (Real Emails)

To send real emails in production, add these to your `.env` file:

```env
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@zambiannrc.gov.zm
```

**For Gmail:**
1. Enable 2-Factor Authentication
2. Generate an App Password
3. Use the App Password (not your regular password)
4. Guide: https://support.google.com/accounts/answer/185833

**For Other Email Providers:**
- **Outlook/Hotmail**: smtp-mail.outlook.com, port 587
- **Yahoo**: smtp.mail.yahoo.com, port 587
- **Custom SMTP**: Contact your email provider

## Files Created

### Templates
1. `templates/accounts/password_reset.html` - Reset request form
2. `templates/accounts/password_reset_done.html` - Email sent confirmation
3. `templates/accounts/password_reset_confirm.html` - New password form
4. `templates/accounts/password_reset_complete.html` - Success page
5. `templates/accounts/password_reset_email.html` - Email template
6. `templates/accounts/password_reset_subject.txt` - Email subject

### Backend
1. `accounts/views.py` - Added password reset views
2. `accounts/urls.py` - Added password reset URLs
3. `nrc_system/settings.py` - Added email configuration

### Updated
1. `templates/accounts/login.html` - Added "Forgot Password" link

## URLs Added

```
/accounts/password-reset/                          - Request reset
/accounts/password-reset/done/                     - Email sent confirmation
/accounts/password-reset-confirm/<uidb64>/<token>/ - Set new password
/accounts/password-reset-complete/                 - Success page
```

## Testing the Feature

### Test in Development:

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Go to login page:**
   ```
   http://127.0.0.1:8000/accounts/login/
   ```

3. **Click "Forgot your password?"**

4. **Enter a user's email address**

5. **Check the console/terminal** for the reset email

6. **Copy the reset link** from the console

7. **Paste the link** in your browser

8. **Enter new password** twice

9. **Login with new password**

## Troubleshooting

### Issue: "No email received"
**Solution**: In development mode, check your console/terminal output

### Issue: "Invalid reset link"
**Solution**: 
- Link may have expired (24 hours)
- Link may have been used already
- Request a new reset link

### Issue: "Password doesn't meet requirements"
**Solution**: 
- Must be at least 8 characters
- Can't be too similar to username
- Can't be entirely numeric
- Can't be too common

### Issue: "Email not found"
**Solution**: 
- Check if the email is registered
- Try the email used during signup
- Contact admin if needed

## Security Best Practices

### For Users:
1. Use a strong, unique password
2. Don't share your password
3. Don't reuse passwords from other sites
4. Change password if you suspect compromise

### For Administrators:
1. Monitor password reset requests
2. Set up email alerts for suspicious activity
3. Use HTTPS in production
4. Keep Django and dependencies updated
5. Configure proper email authentication

## Customization

### Change Reset Link Expiry Time

Edit `nrc_system/settings.py`:
```python
# Change from 24 hours to desired time (in seconds)
PASSWORD_RESET_TIMEOUT = 86400  # 24 hours
PASSWORD_RESET_TIMEOUT = 3600   # 1 hour
PASSWORD_RESET_TIMEOUT = 172800 # 48 hours
```

### Customize Email Template

Edit `templates/accounts/password_reset_email.html` to change:
- Email content
- Styling
- Additional information
- Branding

### Change Email Subject

Edit `templates/accounts/password_reset_subject.txt`

## Production Checklist

Before deploying to production:

- [ ] Set `DEBUG=False` in settings
- [ ] Configure real SMTP email settings
- [ ] Test email delivery
- [ ] Set up HTTPS
- [ ] Configure proper domain in email links
- [ ] Test the complete flow
- [ ] Set up email monitoring
- [ ] Configure email rate limiting

## Support

If users have issues:
1. Check if email is registered
2. Verify email settings are correct
3. Check spam/junk folder
4. Try different browser
5. Clear browser cache
6. Contact system administrator

---

**Password reset feature is now fully functional and ready to use!** 🔐✨
