# 🔐 Google OAuth Login - Complete Guide

## 📋 Overview

Your NRC System now supports **Google OAuth login**, allowing users to sign in with their Google account in one click - no password needed!

## ✨ Features

- ✅ One-click Google sign-in
- ✅ Automatic account creation
- ✅ Secure OAuth 2.0 authentication
- ✅ Mobile-friendly
- ✅ No password management needed
- ✅ Works alongside traditional login

## 🚀 Quick Start (Choose One)

### Option 1: Super Quick (6 minutes)
Follow: **DEPLOY_GOOGLE_OAUTH_NOW.md**

### Option 2: Detailed Setup (10 minutes)
Follow: **GOOGLE_OAUTH_SETUP.md**

### Option 3: Checklist Approach
Follow: **GOOGLE_OAUTH_CHECKLIST.md**

## 📁 Files Added/Modified

### New Files
- `GOOGLE_OAUTH_SETUP.md` - Complete setup guide
- `QUICK_GOOGLE_OAUTH.md` - 5-minute quick start
- `GOOGLE_OAUTH_CHECKLIST.md` - Step-by-step checklist
- `GOOGLE_OAUTH_SUMMARY.md` - Technical implementation details
- `DEPLOY_GOOGLE_OAUTH_NOW.md` - Fastest deployment guide
- `accounts/management/commands/setup_google_oauth.py` - Auto-setup command
- `.env.example` - Environment variables template

### Modified Files
- `requirements.txt` - Added django-allauth
- `nrc_system/settings.py` - Added allauth configuration
- `nrc_system/urls.py` - Added allauth URLs
- `templates/accounts/login.html` - Added Google button
- `templates/accounts/signup.html` - Added Google button

## 🎯 What You Need

1. **Google Cloud Console Account** (free)
2. **5 minutes** to set up
3. **Client ID and Secret** from Google

## 📸 What It Looks Like

### Login Page
```
┌─────────────────────────────────┐
│     Sign in to your account     │
├─────────────────────────────────┤
│  Username: [____________]       │
│  Password: [____________]       │
│  [Sign in]                      │
│                                 │
│  ─────── Or continue with ───── │
│                                 │
│  [🔵 Sign in with Google]      │
└─────────────────────────────────┘
```

## 🔧 Environment Variables

Add these to Render:

```env
GOOGLE_CLIENT_ID=your-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-secret
SITE_DOMAIN=nrccard.onrender.com
```

## 🧪 Testing Locally

1. Get Google credentials
2. Add to `.env` file:
   ```env
   GOOGLE_CLIENT_ID=your-id
   GOOGLE_CLIENT_SECRET=your-secret
   SITE_DOMAIN=localhost:8000
   ```
3. Run migrations: `python manage.py migrate`
4. Run server: `python manage.py runserver`
5. Visit: http://localhost:8000/accounts/login/

## 🌐 Production Deployment

### Step 1: Deploy Code
```bash
git add .
git commit -m "Add Google OAuth"
git push origin main
```

### Step 2: Add Environment Variables
In Render dashboard → Environment → Add:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `SITE_DOMAIN`

### Step 3: Configure in Admin
Visit: https://nrccard.onrender.com/admin/
- Update Site domain
- Add Social Application

### Step 4: Test
Visit: https://nrccard.onrender.com/accounts/login/

## 🐛 Troubleshooting

### "Sign in with Google" button doesn't appear
- Check django-allauth is installed
- Verify templates have `{% load socialaccount %}`
- Clear browser cache

### "redirect_uri_mismatch" error
- Check redirect URI in Google Console matches exactly:
  `https://nrccard.onrender.com/accounts/google/login/callback/`
- Note the trailing slash!

### "Social application not found"
- Configure Social Application in Django admin
- Verify Client ID and Secret are correct
- Check Site is selected in Social Application

### Users can't sign up
- Set `SOCIALACCOUNT_AUTO_SIGNUP = True` in settings
- Set email verification to 'optional' or 'none'

## 🔒 Security

- ✅ OAuth 2.0 standard protocol
- ✅ Client Secret never exposed to users
- ✅ HTTPS required in production
- ✅ CSRF protection enabled
- ✅ Tokens stored securely

## 📚 Additional Resources

- [Django Allauth Docs](https://django-allauth.readthedocs.io/)
- [Google OAuth Guide](https://developers.google.com/identity/protocols/oauth2)
- [OAuth 2.0 Explained](https://oauth.net/2/)

## 🎉 Success Criteria

You'll know it's working when:
1. ✅ "Sign in with Google" button appears on login page
2. ✅ Clicking it redirects to Google
3. ✅ After Google login, user is redirected back
4. ✅ User account is created automatically
5. ✅ User can access protected pages

## 🚀 Next Steps

After Google OAuth is working:
- Add Facebook login (similar process)
- Add GitHub login
- Show user's Google profile picture
- Allow users to disconnect accounts

## 💡 Tips

- Test in incognito/private window to avoid cache issues
- Use different Google accounts to test multiple users
- Check Django logs for detailed error messages
- Keep Client Secret secure - never commit to Git

## 📞 Support

If you need help:
1. Check the troubleshooting section above
2. Review GOOGLE_OAUTH_SETUP.md
3. Check Django logs for errors
4. Verify all environment variables are set

---

**Made with ❤️ for the Zambian NRC System**

**Ready to deploy?** Start with DEPLOY_GOOGLE_OAUTH_NOW.md
