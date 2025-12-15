# 🚨 URGENT SECURITY FIX - SMTP CREDENTIALS EXPOSED

## IMMEDIATE ACTIONS REQUIRED

### 1. **Generate New Gmail App Password** (DO THIS NOW!)

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** → **2-Step Verification**
3. Scroll down to **App passwords**
4. **DELETE the old app password** (the exposed one: feirlikfycpiddbw)
5. Generate a **NEW** app password:
   - Select app: **Mail**
   - Select device: **Other (Custom name)**
   - Name: **NRC System New**
   - Copy the new 16-character password

### 2. **Update Local Environment**

1. Open your `.env` file
2. Replace the email settings with your NEW credentials:
```
EMAIL_HOST_USER=simoongalaurent427@gmail.com
EMAIL_HOST_PASSWORD=YOUR_NEW_16_CHAR_PASSWORD_HERE
DEFAULT_FROM_EMAIL=simoongalaurent427@gmail.com
```

### 3. **Update Production Environment (Render.com)**

1. Go to your Render.com dashboard
2. Select your NRC System service
3. Go to **Environment** tab
4. Update these environment variables:
   - `EMAIL_HOST_USER=simoongalaurent427@gmail.com`
   - `EMAIL_HOST_PASSWORD=YOUR_NEW_16_CHAR_PASSWORD`
   - `EMAIL_HOST=smtp.gmail.com`
   - `EMAIL_PORT=587`
   - `EMAIL_USE_TLS=True`
   - `DEFAULT_FROM_EMAIL=simoongalaurent427@gmail.com`

### 4. **Clean Git History** (CRITICAL!)

The old credentials are still in your Git history. You need to:

1. **Option A: Force push clean history** (RECOMMENDED)
```bash
# Create a new branch without the sensitive data
git checkout --orphan clean-main
git add -A
git commit -m "Clean repository - removed exposed credentials"
git branch -D main
git branch -m main
git push -f origin main
```

2. **Option B: Use BFG Repo-Cleaner** (Advanced)
```bash
# Download BFG: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --replace-text passwords.txt
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

### 5. **Verify Security Fix**

1. Check GitHub repository - ensure no credentials visible
2. Test OTP emails locally with new password
3. Test OTP emails in production
4. Monitor for any GitGuardian alerts

## WHY THIS HAPPENED

- The `.env` file with real credentials was accidentally committed to GitHub
- GitGuardian detected the exposed SMTP credentials
- Gmail may have automatically disabled the app password for security
- Production environment needs the new credentials

## PREVENTION MEASURES

✅ `.env` is already in `.gitignore`
✅ Use `.env.example` for templates
✅ Never commit real credentials
✅ Use environment variables in production
✅ Regular security audits

## IMMEDIATE NEXT STEPS

1. **Generate new Gmail app password** (5 minutes)
2. **Update production environment variables** (5 minutes)  
3. **Test OTP functionality** (5 minutes)
4. **Clean Git history** (10 minutes)

## PRODUCTION ENVIRONMENT VARIABLES NEEDED

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=simoongalaurent427@gmail.com
EMAIL_HOST_PASSWORD=YOUR_NEW_APP_PASSWORD
DEFAULT_FROM_EMAIL=simoongalaurent427@gmail.com
```

## TESTING AFTER FIX

1. Try logging in to your production site
2. Request OTP verification
3. Check if email arrives
4. Verify OTP works correctly

**⚠️ CRITICAL: Do not commit any real credentials to Git again!**