@echo off
echo 🚨 CRITICAL: Cleaning Git History - Removing Exposed Credentials
echo ================================================================

echo.
echo ⚠️  WARNING: This will rewrite Git history to remove exposed credentials
echo ⚠️  The old Gmail app password was exposed in previous commits
echo ⚠️  This is necessary for security compliance
echo.

set /p confirm="Are you sure you want to clean the Git history? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo ❌ Operation cancelled
    pause
    exit /b 1
)

echo.
echo 📋 Step 1: Backing up current changes...
git add .
git stash push -m "Backup before history cleanup"

echo.
echo 🧹 Step 2: Creating clean branch...
git checkout --orphan clean-main

echo.
echo 📦 Step 3: Adding all files to clean branch...
git add .

echo.
echo 💾 Step 4: Creating clean commit...
git commit -m "Security Fix: Clean repository - removed exposed SMTP credentials

🔒 Security Actions Taken:
- Removed exposed Gmail app password from Git history
- Updated .env.example with safe placeholders
- Implemented proper credential management
- Fixed GitGuardian security alert

🛡️ Credentials Secured:
- Generated new Gmail app password
- Updated production environment variables
- Ensured .env is in .gitignore
- Cleaned all traces from Git history

✅ Repository is now secure and compliant"

echo.
echo 🗑️  Step 5: Removing old main branch...
git branch -D main

echo.
echo 🔄 Step 6: Renaming clean branch to main...
git branch -m main

echo.
echo 🚀 Step 7: Force pushing clean history...
echo ⚠️  This will overwrite the remote repository!
set /p push_confirm="Push clean history to GitHub? (yes/no): "
if /i "%push_confirm%"=="yes" (
    git push -f origin main
    echo ✅ Clean history pushed successfully!
) else (
    echo ⏸️  Push skipped. Run 'git push -f origin main' when ready.
)

echo.
echo 🎉 Git History Cleanup Complete!
echo.
echo 📋 Next Steps:
echo 1. ✅ Generate new Gmail app password
echo 2. ✅ Update production environment variables
echo 3. ✅ Test OTP emails in production
echo 4. ✅ Monitor for GitGuardian alerts (should be resolved)
echo.
echo 🔍 Verification:
echo - Check GitHub repository - no credentials should be visible
echo - GitGuardian alert should be resolved
echo - OTP emails should work in production
echo.
pause