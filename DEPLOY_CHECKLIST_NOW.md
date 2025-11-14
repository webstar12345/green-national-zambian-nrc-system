# Deploy to Render - Quick Checklist

## ✅ Pre-Deployment (Do This First)

### 1. Create GitHub Repository
- [ ] Go to https://github.com
- [ ] Click "+" → "New repository"
- [ ] Name: `zambian-nrc-system`
- [ ] Make it Public
- [ ] **DO NOT** initialize with README
- [ ] Click "Create repository"
- [ ] **Copy the repository URL** (you'll need it!)

### 2. Push Code to GitHub (Use Git Bash)

Open Git Bash in your project folder and run:

```bash
# Configure git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# Initialize and push
git init
git add .
git commit -m "Initial commit - Zambian NRC System"
git remote add origin https://github.com/YOUR_USERNAME/zambian-nrc-system.git
git branch -M main
git push -u origin main
```

**If asked for credentials:**
- Username: Your GitHub username
- Password: Use Personal Access Token (create at https://github.com/settings/tokens)

---

## ✅ Render Deployment

### 3. Create Render Account
- [ ] Go to https://render.com
- [ ] Sign up with GitHub (easiest)
- [ ] Authorize Render

### 4. Create PostgreSQL Database
- [ ] Click "New +" → "PostgreSQL"
- [ ] Name: `zambian-nrc-db`
- [ ] Region: Frankfurt
- [ ] Plan: Free
- [ ] Click "Create Database"
- [ ] **Wait 1-2 minutes**
- [ ] Copy "Internal Database URL" (save it!)

### 5. Create Web Service
- [ ] Click "New +" → "Web Service"
- [ ] Connect your GitHub repository
- [ ] Select `zambian-nrc-system`

**Configuration:**
- Name: `zambian-nrc-system`
- Region: Frankfurt
- Branch: `main`
- Build Command: `./build.sh`
- Start Command: `gunicorn nrc_system.wsgi:application`
- Plan: Free

### 6. Add Environment Variables

Click "Advanced" and add these:

**SECRET_KEY:**
```python
# Generate in Python:
import secrets
print(secrets.token_urlsafe(50))
```
Copy the output

**Add these variables:**
```
SECRET_KEY=<paste generated key>
DEBUG=False
DATABASE_URL=<paste Internal Database URL>
ALLOWED_HOSTS=zambian-nrc-system.onrender.com
GEMINI_API_KEY=AIzaSyAOmQ21LSQMA9u0OB_3fBFeeU3moS6jyNk
```

### 7. Deploy
- [ ] Click "Create Web Service"
- [ ] Wait 5-10 minutes
- [ ] Watch logs for errors

---

## ✅ Post-Deployment

### 8. Create Superuser
- [ ] Go to your web service
- [ ] Click "Shell" tab
- [ ] Run: `python manage.py createsuperuser`
- [ ] Enter username, email, password

### 9. Test Your Site
- [ ] Visit: `https://zambian-nrc-system.onrender.com`
- [ ] Test login
- [ ] Test signup
- [ ] Test NRC application
- [ ] Test admin: `/admin`
- [ ] Test AI chat
- [ ] Test password reset

---

## 🎉 You're Live!

Your site is now accessible at:
**https://zambian-nrc-system.onrender.com**

(Replace with your actual service name)

---

## 📝 Important Notes

**Free Tier:**
- Service sleeps after 15 min inactivity
- First request takes 30-60 seconds to wake
- Database free for 90 days

**Upgrade to Paid ($7/month):**
- Always on
- Faster response
- Better for production

---

## 🆘 Troubleshooting

**Build Failed?**
```bash
chmod +x build.sh
git add build.sh
git commit -m "Fix build.sh permissions"
git push
```

**Static files not loading?**
- Check build logs
- Verify collectstatic ran

**Database error?**
- Use Internal Database URL (not External)
- Check DATABASE_URL is correct

**502 Error?**
- Check logs in Render dashboard
- Verify start command is correct

---

## 📞 Need Help?

- Full guide: `DEPLOY_NOW_GUIDE.md`
- Render docs: https://render.com/docs
- Community: https://community.render.com

---

**Good luck with your deployment! 🚀🇿🇲**
