# Google OAuth Setup Checklist

Use this checklist to ensure everything is set up correctly.

## ✅ Pre-Deployment

- [ ] Code changes committed
- [ ] `django-allauth` added to requirements.txt
- [ ] Settings updated with allauth configuration
- [ ] Templates updated with Google login buttons
- [ ] Management command created

## ✅ Google Cloud Console

- [ ] Created Google Cloud project
- [ ] Enabled Google+ API
- [ ] Configured OAuth consent screen
- [ ] Created OAuth Client ID
- [ ] Added authorized redirect URIs:
  - [ ] `http://localhost:8000/accounts/google/login/callback/`
  - [ ] `https://nrccard.onrender.com/accounts/google/login/callback/`
- [ ] Copied Client ID
- [ ] Copied Client Secret

## ✅ Environment Variables

### Local (.env file)
- [ ] Added `GOOGLE_CLIENT_ID`
- [ ] Added `GOOGLE_CLIENT_SECRET`
- [ ] Added `SITE_DOMAIN=localhost:8000`

### Production (Render)
- [ ] Added `GOOGLE_CLIENT_ID` to Render environment
- [ ] Added `GOOGLE_CLIENT_SECRET` to Render environment
- [ ] Added `SITE_DOMAIN=nrccard.onrender.com` to Render environment

## ✅ Deployment

- [ ] Pushed code to GitHub
- [ ] Render deployment completed successfully
- [ ] No build errors
- [ ] Migrations ran successfully

## ✅ Django Admin Configuration

- [ ] Logged into Django admin
- [ ] Updated Site domain to `nrccard.onrender.com`
- [ ] Created Social Application for Google
- [ ] Added Client ID to Social Application
- [ ] Added Client Secret to Social Application
- [ ] Selected site in Social Application

## ✅ Testing

- [ ] Visited login page
- [ ] "Sign in with Google" button appears
- [ ] Clicked Google login button
- [ ] Redirected to Google login
- [ ] Successfully logged in
- [ ] Redirected back to site
- [ ] User account created automatically
- [ ] Can access protected pages

## ✅ Optional Enhancements

- [ ] Tested signup with Google
- [ ] Verified user profile shows Google info
- [ ] Tested logout and re-login
- [ ] Tested on mobile device
- [ ] Added Google profile picture to user profile
- [ ] Configured email verification settings

## 🎉 Success!

If all items are checked, your Google OAuth login is fully functional!

---

**Having issues?** Check GOOGLE_OAUTH_SETUP.md for troubleshooting tips.
