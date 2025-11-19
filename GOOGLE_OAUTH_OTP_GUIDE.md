# Google OAuth with OTP Verification - Complete Guide

## 🔐 What This Does

Adds **Google Sign-In** with **email OTP verification** for extra security:

1. User clicks "Sign in with Google"
2. Authenticates with Google
3. Receives 6-digit OTP code via email
4. Enters OTP to complete login
5. Successfully logged in!

## 🚀 Quick Setup (15 minutes)

### Step 1: Create Database Migration

Run this in Git Bash:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Set Up Google OAuth

1. **Go to Google Cloud Console:**
   https://console.cloud.google.com

2. **Create a New Project:**
   - Click "Select a project" → "New Project"
   - Name: "NRC Zambia"
   - Click "Create"

3. **Enable Google+ API:**
   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API"
   - Click "Enable"

4. **Create OAuth Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Web application"
   - Name: "NRC Zambia Web"
   
5. **Add Authorized URLs:**
   
   **Authorized JavaScript origins:**
   ```
   http://localhost:8000
   https://nrccard.onrender.com
   ```
   
   **Authorized redirect URIs:**
   ```
   http://localhost:8000/accounts/google/login/callback/
   https://nrccard.onrender.com/accounts/google/login/callback/
   ```

6. **Copy Credentials:**
   - Client ID: `123456789-abc...apps.googleusercontent.com`
   - Client Secret: `GOCSPX-abc...`

### Step 3: Configure Email (Gmail)

1. **Enable 2-Step Verification:**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Create App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" → "NRC Zambia"
   - Click "Generate"
   - Copy the 16-character password

### Step 4: Add Environment Variables to Render

Go to Render Dashboard → Your Service → Environment → Add these:

```
GOOGLE_CLIENT_ID = your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET = GOCSPX-your-client-secret

EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-16-char-app-password
DEFAULT_FROM_EMAIL = noreply@zambiannrc.gov.zm
```

### Step 5: Deploy

```bash
git add accounts/models.py accounts/views.py accounts/urls.py templates/accounts/login.html templates/accounts/signup.html templates/accounts/google_otp_verify.html GOOGLE_OAUTH_OTP_GUIDE.md
git commit -m "Add Google OAuth with OTP verification"
git push origin main
```

### Step 6: Configure in Django Admin

1. Go to: https://nrccard.onrender.com/admin
2. Login with admin account
3. Go to "Sites" → Click on "example.com"
4. Change:
   - Domain name: `nrccard.onrender.com`
   - Display name: `NRC Zambia`
5. Save

6. Go to "Social applications" → "Add social application"
   - Provider: Google
   - Name: Google OAuth
   - Client id: (paste your Client ID)
   - Secret key: (paste your Client Secret)
   - Sites: Select "nrccard.onrender.com" and move to "Chosen sites"
7. Save

## 🎯 How It Works

### User Flow:

```
1. User clicks "Sign in with Google"
   ↓
2. Redirected to Google login
   ↓
3. User logs in with Google
   ↓
4. System generates 6-digit OTP
   ↓
5. OTP sent to user's email
   ↓
6. User redirected to OTP verification page
   ↓
7. User enters OTP code
   ↓
8. System verifies OTP (valid for 10 minutes)
   ↓
9. User logged in successfully!
```

### Security Features:

✅ **Two-Factor Authentication** - Google + OTP
✅ **Time-Limited OTP** - Expires in 10 minutes
✅ **One-Time Use** - OTP deleted after verification
✅ **Email Verification** - Confirms email ownership
✅ **Secure Storage** - OTP hashed in database

## 📧 Email Template

Users receive this email:

```
Subject: NRC Zambia - Login Verification Code

Hello,

Your verification code for NRC Zambia login is: 123456

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
NRC Zambia Team
```

## 🧪 Testing

### Local Testing:

1. Run server: `python manage.py runserver`
2. Go to: http://localhost:8000/accounts/login
3. Click "Sign in with Google"
4. Login with Google
5. Check your email for OTP
6. Enter OTP code
7. Should be logged in!

### Production Testing:

1. Go to: https://nrccard.onrender.com/accounts/login
2. Click "Sign in with Google"
3. Follow the same steps

## 🐛 Troubleshooting

### "redirect_uri_mismatch" Error

**Problem:** Google OAuth redirect URL doesn't match

**Solution:**
1. Go to Google Cloud Console
2. Check "Authorized redirect URIs"
3. Make sure you have:
   ```
   https://nrccard.onrender.com/accounts/google/login/callback/
   ```
4. Note the trailing slash!

### OTP Email Not Received

**Problem:** Email not sending

**Solutions:**
1. Check Gmail App Password is correct
2. Verify EMAIL_HOST_USER is your Gmail
3. Check Render logs for email errors
4. Make sure 2-Step Verification is enabled

### "Site matching query does not exist"

**Problem:** Django site not configured

**Solution:**
1. Go to Django admin
2. Sites → Edit "example.com"
3. Change to your domain
4. Save

### OTP Always Invalid

**Problem:** Time sync or code mismatch

**Solutions:**
1. Check server time is correct
2. Make sure you're entering all 6 digits
3. Try resending OTP
4. Check OTP hasn't expired (10 min limit)

## 📊 Database Fields Added

New fields in `CustomUser` model:

```python
otp_code = CharField(max_length=6)  # 6-digit code
otp_created_at = DateTimeField()    # When OTP was generated
otp_verified = BooleanField()       # Whether OTP was verified
```

## 🔒 Security Best Practices

1. **Never share OTP codes**
2. **OTP expires in 10 minutes**
3. **One-time use only**
4. **Sent to verified email only**
5. **Secure HTTPS connection**

## 💡 Features

✅ **Google Sign-In** - Quick authentication
✅ **Email OTP** - Extra security layer
✅ **Auto-submit** - When 6 digits entered
✅ **Resend OTP** - If code not received
✅ **Expiration** - 10-minute validity
✅ **User-friendly** - Clear instructions
✅ **Mobile responsive** - Works on all devices

## 📱 User Experience

### Login Page:
- Regular username/password login
- OR
- "Sign in with Google (OTP Required)" button
- Clear security notice

### OTP Page:
- Clean, focused design
- Large OTP input field
- Auto-submit when complete
- Resend option
- Back to login link
- Security notice

## 🎨 UI Features

- **Auto-focus** on OTP input
- **Auto-submit** when 6 digits entered
- **Number-only** input validation
- **Visual feedback** for errors/success
- **Countdown timer** (optional enhancement)
- **Dark mode** support

## 📞 Support

If users have issues:

1. **Can't receive OTP:**
   - Check spam folder
   - Click "Resend Code"
   - Verify email address

2. **OTP expired:**
   - Click "Resend Code"
   - Enter new code within 10 minutes

3. **Still can't login:**
   - Use regular username/password
   - Contact support

## ✅ Checklist

- [ ] Created Google Cloud project
- [ ] Enabled Google+ API
- [ ] Created OAuth credentials
- [ ] Added authorized URLs
- [ ] Set up Gmail App Password
- [ ] Added environment variables to Render
- [ ] Ran database migrations
- [ ] Configured Django admin (Sites)
- [ ] Configured Django admin (Social apps)
- [ ] Tested Google login
- [ ] Received OTP email
- [ ] Successfully verified OTP
- [ ] Logged in successfully

## 🎉 Done!

Your NRC System now has **secure Google OAuth with OTP verification**! Users can sign in with Google and receive email verification codes for extra security.

---

**Next Steps:**
1. Complete setup (15 minutes)
2. Test thoroughly
3. Inform users about new login option
4. Monitor email delivery
5. Enjoy secure authentication! 🔐
