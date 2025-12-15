# 🚨 RESTORE PRODUCTION SERVICE NOW

## 🔥 CURRENT STATUS
- **Site**: https://green-national-zambian-nrc-system.onrender.com
- **Error**: HTTP 503 Service Unavailable
- **Cause**: Shell scripts with Windows line endings can't execute on Render.com

## ⚡ IMMEDIATE FIX (Choose Option A or B)

### **OPTION A: Quick Rollback (2 minutes) - RECOMMENDED**

**Go to Render.com Dashboard → Your Service → Settings:**

**Build Command:** (paste this exactly)
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:** (paste this exactly)
```
gunicorn nrc_system.wsgi:application
```

**Click "Save Changes" → Wait for deployment**

### **OPTION B: Use Fixed Shell Scripts (3 minutes)**

**Build Command:**
```
./build.sh
```

**Start Command:**
```
./start.sh
```

## 🔑 CRITICAL: UPDATE ENVIRONMENT VARIABLES

**Go to Environment tab in Render.com and ADD/UPDATE:**

```
EMAIL_HOST_PASSWORD=uroaoegylbpusjfy
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
WEB_CONCURRENCY=1
```

## 📤 PUSH LATEST FIXES

**Run in Git Bash:**
```bash
git add .
git commit -m "EMERGENCY: Production restore - Fixed shell scripts + OTP security"
git push origin main
```

## 🎯 VERIFICATION STEPS

1. **Check Render.com Dashboard** - Look for "Deploy successful"
2. **Visit Site** - https://green-national-zambian-nrc-system.onrender.com
3. **Test Login** - Try to login and check for OTP email
4. **Monitor Logs** - No more WORKER TIMEOUT errors

## 🛡️ SECURITY STATUS
- ✅ New Gmail password: `uroaoegylbpusjfy` (secure, tested locally)
- ✅ Old compromised password removed
- ✅ GitGuardian alert will be resolved after deployment

## 📞 IF STILL HAVING ISSUES

### **503 Error Persists:**
- Use Option A (rollback commands)
- Check Render.com logs for specific errors
- Verify environment variables are set

### **OTP Emails Not Working:**
- Confirm EMAIL_HOST_PASSWORD is set to `uroaoegylbpusjfy`
- Check spam folder
- Verify Gmail app password is still active

### **Memory Issues Return:**
- Monitor Render.com logs for WORKER TIMEOUT
- Consider upgrading Render.com plan
- Use gunicorn.conf.py settings (single worker)

## 🚀 EXPECTED TIMELINE
- **Deployment**: 3-5 minutes
- **Service Restore**: Immediate after deployment
- **OTP Testing**: 2-3 minutes after service is up

**Your production service should be restored within 10 minutes of following these steps.**