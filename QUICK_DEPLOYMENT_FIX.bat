@echo off
echo ========================================
echo  QUICK DEPLOYMENT FIX
echo ========================================
echo.

echo Fixing migration dependency and pushing...
echo.

git add accounts/migrations/0004_add_otp_fields_fixed.py
git add applications/migrations/0008_add_collection_location.py

git commit -m "Fix deployment migration error - correct dependencies"

git push origin main

echo.
echo ========================================
echo  FIX PUSHED!
echo ========================================
echo.
echo Your Render deployment should now succeed!
echo Check your dashboard for the updated deployment.
echo.
pause