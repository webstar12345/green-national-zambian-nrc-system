# Render Deployment Guide - Zambian NRC System

## Overview
This guide will help you deploy your Zambian NRC System to Render, a modern cloud platform for hosting web applications.

## Prerequisites
- GitHub account
- Render account (free tier available)
- Your project code ready

## Step 1: Prepare Your Project

### 1.1 Create a GitHub Repository
1. Go to https://github.com
2. Click "New Repository"
3. Name it: `zambian-nrc-system`
4. Make it Public or Private
5. Don't initialize with README (we have one)
6. Click "Create Repository"

### 1.2 Push Your Code to GitHub

Open your terminal in the project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Zambian NRC System"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/zambian-nrc-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Create Render Account

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

## Step 3: Create PostgreSQL Database

### 3.1 Create Database
1. In Render Dashboard, click "New +"
2. Select "PostgreSQL"
3. Fill in details:
   - **Name**: `zambian-nrc-db`
   - **Database**: `nrc_database`
   - **User**: `nrc_user` (auto-generated)
   - **Region**: Choose closest to Zambia (e.g., Frankfurt)
   - **Plan**: Free
4. Click "Create Database"

### 3.2 Get Database URL
1. Wait for database to be created (1-2 minutes)
2. Click on your database
3. Scroll down to "Connections"
4. Copy the "Internal Database URL"
5. Save it somewhere safe (you'll need it)

## Step 4: Create Web Service

### 4.1 Create New Web Service
1. In Render Dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Select `zambian-nrc-system`

### 4.2 Configure Web Service
Fill in the following:

**Basic Settings:**
- **Name**: `zambian-nrc-system`
- **Region**: Same as database (e.g., Frankfurt)
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn nrc_system.wsgi:application`

**Plan:**
- Select "Free" (or paid plan for better performance)

### 4.3 Add Environment Variables
Click "Advanced" and add these environment variables:

```
SECRET_KEY=your-super-secret-key-here-change-this-to-random-string
DEBUG=False
DATABASE_URL=<paste-your-internal-database-url-here>
ALLOWED_HOSTS=your-app-name.onrender.com
GEMINI_API_KEY=<your-gemini-api-key>
```

**To generate a SECRET_KEY:**
```python
# Run this in Python
import secrets
print(secrets.token_urlsafe(50))
```

### 4.4 Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Watch the logs for any errors

## Step 5: Post-Deployment Setup

### 5.1 Create Superuser
1. Go to your Render Dashboard
2. Click on your web service
3. Click "Shell" tab
4. Run:
```bash
python manage.py createsuperuser
```
5. Follow prompts to create admin account

### 5.2 Test Your Site
1. Click "Open" or visit: `https://your-app-name.onrender.com`
2. Test login, signup, and main features
3. Access admin: `https://your-app-name.onrender.com/admin`

## Step 6: Configure Custom Domain (Optional)

### 6.1 Add Custom Domain
1. In Render Dashboard, go to your web service
2. Click "Settings"
3. Scroll to "Custom Domains"
4. Click "Add Custom Domain"
5. Enter your domain (e.g., `nrc.gov.zm`)

### 6.2 Update DNS
1. Go to your domain registrar
2. Add CNAME record:
   - **Name**: `www` or `@`
   - **Value**: `your-app-name.onrender.com`
3. Wait for DNS propagation (up to 48 hours)

### 6.3 Update ALLOWED_HOSTS
Add your custom domain to environment variables:
```
ALLOWED_HOSTS=your-app-name.onrender.com,nrc.gov.zm,www.nrc.gov.zm
```

## Step 7: Configure Email (Optional)

For password reset emails to work, add these environment variables:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@zambiannrc.gov.zm
```

**For Gmail:**
1. Enable 2-Factor Authentication
2. Generate App Password
3. Use App Password (not regular password)

## Troubleshooting

### Issue: Build Failed
**Check:**
- `requirements.txt` is correct
- `build.sh` has execute permissions
- Python version in `runtime.txt` is supported

**Solution:**
```bash
# Make build.sh executable
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### Issue: Static Files Not Loading
**Check:**
- WhiteNoise is in MIDDLEWARE
- STATIC_ROOT is set correctly
- `collectstatic` runs in build.sh

**Solution:**
- Check build logs for errors
- Verify STATICFILES_STORAGE setting

### Issue: Database Connection Error
**Check:**
- DATABASE_URL is correct
- Database is running
- Internal URL is used (not External)

**Solution:**
- Copy Internal Database URL again
- Update environment variable
- Redeploy

### Issue: 502 Bad Gateway
**Check:**
- Start command is correct
- gunicorn is installed
- Application starts without errors

**Solution:**
- Check logs in Render Dashboard
- Verify WSGI application path

## Monitoring and Maintenance

### View Logs
1. Go to Render Dashboard
2. Click your web service
3. Click "Logs" tab
4. Monitor for errors

### Update Your App
```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push

# Render will auto-deploy
```

### Backup Database
1. Go to your database in Render
2. Click "Backups" tab
3. Click "Create Backup"
4. Download backup file

## Performance Tips

### 1. Upgrade to Paid Plan
- Free tier sleeps after inactivity
- Paid plans are always on
- Better performance

### 2. Use CDN for Static Files
- Consider Cloudflare
- Faster static file delivery
- Better global performance

### 3. Enable Caching
- Add Redis for caching
- Cache database queries
- Improve response times

### 4. Optimize Database
- Add indexes
- Optimize queries
- Regular maintenance

## Security Checklist

- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY
- [ ] HTTPS enabled (automatic on Render)
- [ ] ALLOWED_HOSTS configured
- [ ] Database password secure
- [ ] Environment variables set
- [ ] Regular backups enabled
- [ ] Monitor logs for suspicious activity

## Cost Estimate

**Free Tier:**
- Web Service: Free (sleeps after 15 min inactivity)
- PostgreSQL: Free (90 days, then $7/month)
- Total: $0 for 90 days, then $7/month

**Starter Tier:**
- Web Service: $7/month (always on)
- PostgreSQL: $7/month
- Total: $14/month

## Support Resources

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **Render Community**: https://community.render.com/

## Next Steps

After deployment:
1. Test all features thoroughly
2. Set up monitoring
3. Configure backups
4. Add custom domain
5. Set up email
6. Train users
7. Monitor performance

---

**Your Zambian NRC System is now live on Render!** 🎉🚀
