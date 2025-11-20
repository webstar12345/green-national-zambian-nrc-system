# 🗄️ Setup PostgreSQL Database on Render

Your users are losing their accounts because SQLite doesn't persist on Render's free tier. Follow these steps to set up PostgreSQL:

---

## 📋 **Step 1: Create PostgreSQL Database**

1. Go to your **Render Dashboard**: https://dashboard.render.com
2. Click **"New +"** button (top right)
3. Select **"PostgreSQL"**
4. Fill in the details:
   - **Name:** `zambian-nrc-db` (or any name you prefer)
   - **Database:** `nrc_system`
   - **User:** `nrc_user` (auto-generated)
   - **Region:** Choose same as your web service
   - **PostgreSQL Version:** 16 (latest)
   - **Plan:** **Free** (0 GB storage, expires in 90 days)
5. Click **"Create Database"**

---

## 📋 **Step 2: Get Database URL**

1. After creation, click on your new database
2. Scroll down to **"Connections"** section
3. Copy the **"Internal Database URL"** (starts with `postgres://`)
   - Example: `postgres://user:password@hostname/database`

---

## 📋 **Step 3: Add Database URL to Web Service**

1. Go back to your **Web Service** (green-national-zambian-nrc-system)
2. Click **"Environment"** (left sidebar)
3. Click **"Add Environment Variable"**
4. Add:
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the Internal Database URL you copied
5. Click **"Save Changes"**

---

## 📋 **Step 4: Render Will Auto-Deploy**

After saving, Render will automatically:
1. Redeploy your service
2. Run migrations on PostgreSQL
3. Your database is now persistent!

---

## ✅ **Verify It Works**

1. Create a new user account
2. Log out
3. Wait a few minutes (or restart the service)
4. Log back in with the same credentials
5. **It should work!** ✨

---

## 🔄 **Important Notes:**

### **Free PostgreSQL Limitations:**
- **90 days expiration** - Database expires after 90 days
- **Limited storage** - Good for testing/development
- **Automatic backups** - Not included in free tier

### **For Production:**
Consider upgrading to a paid plan ($7/month) for:
- Persistent database (no expiration)
- Automatic backups
- More storage
- Better performance

---

## 🆘 **Troubleshooting:**

### **If migrations fail:**
1. Go to your web service
2. Click **"Shell"** tab
3. Run: `python manage.py migrate`

### **If you need to create a superuser:**
1. In the Shell tab, run:
```bash
python manage.py createsuperuser
```
2. Follow the prompts

---

## 🎉 **Done!**

Your users' accounts will now persist across restarts!
