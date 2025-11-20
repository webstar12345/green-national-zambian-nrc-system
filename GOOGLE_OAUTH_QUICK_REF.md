# Google OAuth - Quick Reference Card

## 🚀 Deploy in 3 Commands

```bash
git add .
git commit -m "Add Google OAuth login"
git push origin main
```

## 🔑 Environment Variables

```env
GOOGLE_CLIENT_ID=your-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-secret
SITE_DOMAIN=nrccard.onrender.com
```

## 📍 Important URLs

| Purpose | URL |
|---------|-----|
| Login Page | `/accounts/login/` |
| OAuth Callback | `/accounts/google/login/callback/` |
| Admin Config | `/admin/socialaccount/socialapp/` |
| Manage Connections | `/accounts/social/connections/` |

## 🛠️ Key Commands

```bash
# Install package
pip install django-allauth==0.57.0

# Run migrations
python manage.py migrate

# Setup OAuth
python manage.py setup_google_oauth

# Test locally
python manage.py runserver
```

## 📚 Documentation Quick Links

| Need | File |
|------|------|
| Start Here | START_GOOGLE_OAUTH.md |
| Fastest Deploy | DEPLOY_GOOGLE_OAUTH_NOW.md |
| Quick Setup | QUICK_GOOGLE_OAUTH.md |
| Full Guide | GOOGLE_OAUTH_SETUP.md |
| Checklist | GOOGLE_OAUTH_CHECKLIST.md |
| Troubleshooting | GOOGLE_OAUTH_SETUP.md |

## 🔧 Google Console Setup

1. Create project at console.cloud.google.com
2. Enable Google+ API
3. OAuth consent screen → External
4. Create OAuth Client ID → Web application
5. Add redirect URI: `https://nrccard.onrender.com/accounts/google/login/callback/`
6. Copy Client ID and Secret

## ⚙️ Django Admin Setup

1. Go to `/admin/`
2. Sites → Edit → Set domain to `nrccard.onrender.com`
3. Social applications → Add:
   - Provider: Google
   - Client ID: (paste)
   - Secret: (paste)
   - Sites: Select your site

## ✅ Success Checklist

- [ ] Code deployed
- [ ] Google Cloud Console configured
- [ ] Environment variables added
- [ ] Django admin configured
- [ ] Google button appears
- [ ] Login works

## 🐛 Common Issues

| Error | Solution |
|-------|----------|
| Button doesn't appear | Check django-allauth installed |
| redirect_uri_mismatch | Verify redirect URI in Google Console |
| Social app not found | Configure in Django admin |
| Invalid client | Check environment variables |

## 📊 Files Modified

- ✅ requirements.txt
- ✅ nrc_system/settings.py
- ✅ nrc_system/urls.py
- ✅ templates/accounts/login.html
- ✅ templates/accounts/signup.html

## 🎯 Testing

### Local
```bash
# Add to .env
GOOGLE_CLIENT_ID=your-id
GOOGLE_CLIENT_SECRET=your-secret
SITE_DOMAIN=localhost:8000

# Run
python manage.py runserver

# Visit
http://localhost:8000/accounts/login/
```

### Production
```
Visit: https://nrccard.onrender.com/accounts/login/
Click: "Sign in with Google"
Verify: Login works
```

## 💡 Pro Tips

- Test in incognito window
- Check Django logs for errors
- Verify trailing slash in redirect URI
- Use different Google accounts to test
- Keep Client Secret secure

## 🎉 Success Indicators

✅ Google button visible  
✅ Redirects to Google  
✅ Returns to site after login  
✅ User account created  
✅ Can access protected pages  

## 📞 Need Help?

1. GOOGLE_OAUTH_SETUP.md → Troubleshooting
2. GOOGLE_OAUTH_CHECKLIST.md → Verify steps
3. Django logs → Check errors
4. Google Console → Verify settings

---

**Total Setup Time: 6 minutes**  
**Difficulty: Easy**  
**Result: Professional OAuth! 🚀**
