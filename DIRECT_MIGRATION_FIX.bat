@echo off
echo ========================================
echo  DIRECT MIGRATION FIX
echo ========================================
echo.

echo Replacing the problematic migration with a new one...
echo.

echo Step 1: Remove old migration...
del accounts\migrations\0004_add_otp_fields_fixed.py

echo Step 2: Add new migration...
git add accounts/migrations/0004_add_otp_security_fields.py

echo Step 3: Commit and push...
git add -A
git commit -m "Fix migration dependency error - replace with new migration"
git push origin main

echo.
echo ========================================
echo  DONE!
echo ========================================
echo.
echo The new migration should deploy successfully!
echo.
pause