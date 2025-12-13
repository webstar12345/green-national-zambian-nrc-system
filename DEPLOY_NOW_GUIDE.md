# Deploy to Render NOW - Step by Step Guide

## Prerequisites Checklist
Before we start, make sure you have:
- [ ] GitHub account (create at https://github.com if you don't have one)
- [ ] Git installed on your computer
- [ ] Your Gemini API key ready

---

## STEP 1: Install Git (If Not Installed)

### Download and Install Git:
1. Go to: https://git-scm.com/download/win
2. Download Git for Windows
3. Run the installer
4. Use default settings (just click Next)
5. Restart your terminal/command prompt

### Verify Git Installation:
```bash
git --version
```
You should see something like: `git version 2.x.x`

---

## STEP 2: Create GitHub Repository

### 2.1 Create Repository on GitHub:
1. Go to https://github.com
2. Click the "+" icon (top right) → "New repository"
3. Fill in:
   - **Repository name**: `zambian-nrc-system`
   - **Description**: "Online National Registration Card System for Zambia"
   - **Visibility**: Public (or Private if you prefer)
   - **DO NOT** check "Initialize with README"
4. Click "Create repository"

### 2.2 Copy the Repository URL:
After creating, you'll see a URL like:
```
https://github.com/YOUR_USERNAME/zambian-nrc-system.git
```
**Copy this URL - you'll need it!**

---

## STEP 3: Push Your Code to GitHub

Open your terminal in the project folder (`C:\Users\Laurent\Desktop\nrccard`) and run these commands:

### 3.1 Initialize Git:
```bash
git init
```

### 3.2 Add All Files:
```bash
git add .
```

### 3.3 Commit:
```bash
git commit -m "Initial commit - Zambian NRC System ready for deployment"
```

### 3.4 Add Remote (Replace YOUR_USERNAME):
```bash
git remote add origin https://github.com/YOUR_USERNAME/zambian-nrc-system.git
```

### 3.5 Push to GitHub:
```bash
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- Username: Your GitHub username
- Password: Use a Personal Access Token (not your password)
  - Create token at: https://github.com/settings/tokens
  - Select "repo" scope
  - Copy and save the token

---

## STEP 4: Create Render Account

### 4.1 Sign Up:
1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub (recommended) or email
4. If using GitHub, authorize Render to access your repositories

### 4.2 Verify Email:
- Check your email and verify your account

---

## STEP 5: Create PostgreSQL Database

### 5.1 Create Database:
1. In Render Dashboard, click "New +" (top right)
2. Select "PostgreSQL"
3. Fill in:
   - **Name**: `zambian-nrc-db`
   - **Database**: `nrc_database`
   - **User**: (auto-generated, leave as is)
   - **Region**: Frankfurt (closest to Zambia)
   - **PostgreSQL Version**: 16 (latest)
   - **Plan**: Free
4. Click "Create Database"

### 5.2 Wait for Database Creation:
- This takes 1-2 minutes
- Status will change from "Creating" to "Available"

### 5.3 Get Database URL:
1. Click on your database name
2. Scroll down to "Connections" section
3. Find "Internal Database URL"
4. Click "Copy" button
5. **SAVE THIS URL** - you'll need it in the next step!

**The URL looks like:**
```
postgresql://user:password@hostname/database
```

---

## STEP 6: Create Web Service

### 6.1 Create Service:
1. In Render Dashboard, click "New +" (top right)
2. Select "Web Service"
3. Click "Connect a repository"
4. Find and select `zambian-nrc-system`
5. Click "Connect"

### 6.2 Configure Service:

**Basic Settings:**
- **Name**: `zambian-nrc-system` (or your preferred name)
- **Region**: Frankfurt (same as database)
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Runtime**: Python 3
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn nrc_system.wsgi:application`

**Instance Type:**
- Select "Free" (or paid for better performance)

### 6.3 Add Environment Variables:

Click "Advanced" button, then add these environment variables:

**Click "Add Environment Variable" for each:**

1. **SECRET_KEY**
   ```
   Value: django-insecure-CHANGE-THIS-TO-RANDOM-STRING-12345678
   ```
   ⚠️ **IMPORTANT**: Generate a secure key:
   - Open Python in terminal: `python`
   - Run: `import secrets; print(secrets.token_urlsafe(50))`
   - Copy the output and use it as SECRET_KEY

2. **DEBUG**
   ```
   Value: False
   ```

3. **DATABASE_URL**
   ```
   Value: <paste your Internal Database URL from Step 5.3>
   ```

4. **ALLOWED_HOSTS**
   ```
   Value: zambian-nrc-system.onrender.com
   ```
   ⚠️ Replace `zambian-nrc-system` with your actual service name

5. **GEMINI_API_KEY**
   ```
   Value: <your Gemini API key>
   ```

### 6.4 Deploy:
1. Click "Create Web Service"
2. Deployment will start automatically
3. Watch the logs - this takes 5-10 minutes

---

## STEP 7: Monitor Deployment

### 7.1 Watch Build Logs:
You'll see logs like:
```
==> Cloning from https://github.com/...
==> Running build command './build.sh'
==> Installing dependencies
==> Collecting static files
==> Running migrations
==> Build successful!
==> Starting service
```

### 7.2 Wait for "Live" Status:
- Status will change from "Building" → "Deploying" → "Live"
- Green dot means it's live!

---

## STEP 8: Create Superuser

### 8.1 Open Shell:
1. In your web service dashboard
2. Click "Shell" tab (top menu)
3. Wait for shell to connect

### 8.2 Create Admin Account:
In the shell, run:
```bash
python manage.py createsuperuser
```

Follow the prompts:
- **Username**: admin (or your choice)
- **Email**: your-email@example.com
- **Password**: (enter a strong password)
- **Password (again)**: (confirm password)

---

## STEP 9: Test Your Live Site!

### 9.1 Access Your Site:
Your site is now live at:
```
https://zambian-nrc-system.onrender.com
```
(Replace with your actual service name)

### 9.2 Test These Features:
- [ ] Homepage loads
- [ ] Signup works
- [ ] Login works
- [ ] Apply for NRC
- [ ] Admin panel: `https://your-app.onrender.com/admin`
- [ ] AI Assistant chat
- [ ] Password reset
- [ ] Image carousel

---

## STEP 10: Important Post-Deployment Tasks

### 10.1 Update ALLOWED_HOSTS:
If you see "Bad Request (400)" errors:
1. Go to your web service settings
2. Find ALLOWED_HOSTS environment variable
3. Make sure it includes your Render URL
4. Save and redeploy

### 10.2 Test Email (Optional):
To enable password reset emails:
1. Add email environment variables (see RENDER_DEPLOYMENT_GUIDE.md)
2. Use Gmail App Password
3. Test password reset feature

### 10.3 Backup Database:
1. Go to your PostgreSQL database
2. Click "Backups" tab
3. Enable automatic backups

---

## Troubleshooting Common Issues

### Issue 1: Build Failed
**Error**: "build.sh: Permission denied"

**Solution**:
```bash
# In your local project
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### Issue 2: Static Files Not Loading
**Check**:
- Build logs show "Collecting static files"
- STATIC_ROOT is set correctly

**Solution**: Redeploy the service

### Issue 3: Database Connection Error
**Check**:
- DATABASE_URL is correct
- Using Internal URL (not External)

**Solution**: Copy Internal Database URL again and update

### Issue 4: 502 Bad Gateway
**Check**:
- Start command is correct
- Service is running

**Solution**: Check logs for errors

---

## Your Live URLs

After successful deployment:

- **Website**: `https://zambian-nrc-system.onrender.com`
- **Admin Panel**: `https://zambian-nrc-system.onrender.com/admin`
- **API Endpoints**: All working automatically

---

## Free Tier Limitations

⚠️ **Important to Know:**
- Free web service sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- Database is free for 90 days, then $7/month
- Consider upgrading to paid tier ($7/month) for always-on service

---

## Next Steps After Deployment

1. **Share the URL** with stakeholders
2. **Create test accounts** for users
3. **Monitor logs** regularly
4. **Set up custom domain** (optional)
5. **Configure email** for password reset
6. **Train administrators** on the system
7. **Gather user feedback**
8. **Plan for scaling** if needed

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/

---

## Congratulations! 🎉

Your Zambian NRC System is now live and accessible to the world!

**Remember to:**
- Keep your SECRET_KEY and database credentials secure
- Monitor your application regularly
- Keep Django and dependencies updated
- Backup your database regularly

---

**Your system is making NRC applications easier for Zambians! 🇿🇲✨**
