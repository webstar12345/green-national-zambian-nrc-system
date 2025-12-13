@echo off
echo ========================================
echo  NUCLEAR HISTORY FIX - Remove Secrets Forever
echo ========================================
echo.

echo WARNING: This will rewrite ALL git history to remove secret files
echo This is the most thorough solution but cannot be undone
echo.

echo Step 1: Backup your current work...
git branch backup-before-nuclear

echo Step 2: Remove secret files from ALL history...
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch git-deploy-commands.txt" --prune-empty --tag-name-filter cat -- --all

echo Step 3: Remove OAuth file from ALL history...
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch WHAT_I_DID_GOOGLE_OAUTH.md" --prune-empty --tag-name-filter cat -- --all

echo Step 4: Clean up filter-branch backup...
git for-each-ref --format="delete %(refname)" refs/original/ | git update-ref --stdin

echo Step 5: Force garbage collection...
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo Step 6: Add all your current files...
git add .

echo Step 7: Commit current state...
git commit -m "Complete NRC System - Clean History

Features:
- AI Assistant (5 languages)
- OTP Security System
- Enhanced Landing Page
- PWA Features
- Database Improvements
- Authentication Enhancements
- Admin Dashboard
- UI/UX Improvements

History cleaned of sensitive files"

echo Step 8: Force push clean history...
git push --force origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  SUCCESS! Clean History Pushed
    echo ========================================
    echo.
    echo Your repository now has:
    echo ✅ All your new features
    echo ✅ Clean history (no secrets)
    echo ✅ Ready for production deployment
    echo.
    echo You can delete the backup branch:
    echo git branch -D backup-before-nuclear
    echo.
) else (
    echo.
    echo Nuclear fix failed. Restore backup:
    echo git checkout backup-before-nuclear
    echo git branch -D main
    echo git checkout -b main
    echo.
    echo Then try METHOD 4 (GitHub web interface)
    echo.
)

pause