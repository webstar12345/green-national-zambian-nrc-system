@echo off
echo ========================================
echo  EMERGENCY RENDER FIX
echo ========================================
echo.

echo Quick fix for Render deployment issue
echo.

echo Removing problematic migration...
git rm accounts/migrations/0004_add_otp_security_fields.py

echo Adding new migration with different number...
git add accounts/migrations/0005_otp_security_update.py

echo Committing fix...
git commit -m "Emergency fix: Replace migration 0004 with 0005 to bypass Render cache"

echo Pushing fix...
git push origin main

echo.
echo DONE! Check Render dashboard for successful deployment.
echo.
pause