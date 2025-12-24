# EMERGENCY DATABASE CONNECTION FIX

## 🚨 Issue: OperationalError - Name or service not known

Your Render application cannot connect to the PostgreSQL database. This is a common issue with database URL configuration.

## 🔧 IMMEDIATE FIX STEPS

### Step 1: Get the Correct Database URL
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Navigate to your **PostgreSQL service** (not web service)
3. In the database service page, find **"Connections"** section
4. Copy the **"External Database URL"** (NOT internal URL)
5. The URL should end with `-a` like: `dpg-xxxxx-a`

### Step 2: Update Web Service Environment
1. Go to your **Web Service** in Render dashboard
2. Click **"Environment"** tab
3. Add or update the environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: [Paste the External Database URL from Step 1]
4. Click **"Save Changes"**

### Step 3: Restart Services
1. Your web service will automatically redeploy
2. Wait for deployment to complete
3. Check if the error is resolved

## 🔍 COMMON ISSUES & SOLUTIONS

### Issue 1: Using Internal URL Instead of External
- **Problem**: Internal URLs (without `-a`) don't work from web services
- **Solution**: Always use External Database URL ending with `-a`

### Issue 2: Missing DATABASE_URL Environment Variable
- **Problem**: Environment variable not set or incorrectly named
- **Solution**: Ensure exact name `DATABASE_URL` (case-sensitive)

### Issue 3: Database Service Not Running
- **Problem**: PostgreSQL service is suspended or failed
- **Solution**: Check database service status and restart if needed

### Issue 4: Incorrect URL Format
- **Problem**: Malformed database URL
- **Solution**: URL should be: `postgresql://user:password@host/database`

## 📋 VERIFICATION CHECKLIST

- [ ] ✅ PostgreSQL service is running and active
- [ ] ✅ Using External Database URL (ends with `-a`)
- [ ] ✅ DATABASE_URL environment variable is set correctly
- [ ] ✅ Web service has been redeployed after changes
- [ ] ✅ No typos in environment variable name or value

## 🛠️ TROUBLESHOOTING COMMANDS

Run this diagnostic script:
```bash
python fix_render_database_connection.py
```

## 📞 IF ISSUE PERSISTS

1. **Check Render Status**: Visit [Render Status Page](https://status.render.com)
2. **Database Logs**: Check your PostgreSQL service logs
3. **Web Service Logs**: Check deployment logs for other errors
4. **Contact Support**: If all else fails, contact Render support

## 🎯 EXPECTED RESULT

After fixing, your application should:
- ✅ Load without database connection errors
- ✅ Display the landing page correctly
- ✅ Allow user authentication and database operations

## ⚡ QUICK REFERENCE

**Correct Database URL Format:**
```
postgresql://username:password@dpg-xxxxxxxxx-a/database_name
```

**Environment Variable:**
- Name: `DATABASE_URL`
- Value: [External Database URL from PostgreSQL service]

---

**Last Updated**: December 24, 2024
**Status**: Emergency Fix for Production Issue