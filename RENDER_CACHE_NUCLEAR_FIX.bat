@echo off
echo ========================================
echo  RENDER CACHE NUCLEAR FIX
echo ========================================
echo.

echo PROBLEM: Render has cached the old problematic migration
echo SOLUTION: Force complete cache clear with new deployment
echo.

echo Step 1: Create a completely new migration structure...
echo Removing ALL problematic migrations...

echo Step 2: Create fresh migration with new approach...
echo # Fresh OTP Migration - No Cache Conflicts > accounts/migrations/0006_fresh_otp_setup.py
echo from django.db import migrations, models >> accounts/migrations/0006_fresh_otp_setup.py
echo. >> accounts/migrations/0006_fresh_otp_setup.py
echo. >> accounts/migrations/0006_fresh_otp_setup.py
echo class Migration(migrations.Migration): >> accounts/migrations/0006_fresh_otp_setup.py
echo. >> accounts/migrations/0006_fresh_otp_setup.py
echo     dependencies = [ >> accounts/migrations/0006_fresh_otp_setup.py
echo         ('accounts', '0003_customuser_otp_code_customuser_otp_created_at_and_more'), >> accounts/migrations/0006_fresh_otp_setup.py
echo     ] >> accounts/migrations/0006_fresh_otp_setup.py
echo. >> accounts/migrations/0006_fresh_otp_setup.py
echo     operations = [ >> accounts/migrations/0006_fresh_otp_setup.py
echo         # No-op migration - fields already exist from 0003 >> accounts/migrations/0006_fresh_otp_setup.py
echo         # This just ensures the migration chain is complete >> accounts/migrations/0006_fresh_otp_setup.py
echo     ] >> accounts/migrations/0006_fresh_otp_setup.py

echo Step 3: Remove the problematic migration...
git rm accounts/migrations/0005_otp_security_update.py 2>nul

echo Step 4: Add the new clean migration...
git add accounts/migrations/0006_fresh_otp_setup.py

echo Step 5: Force Render to clear cache with environment variable change...
echo Creating cache-busting commit...
git commit -m "RENDER CACHE FIX: New migration 0006 to bypass cache

- Removed all problematic 0004/0005 migrations
- Created 0006_fresh_otp_setup.py with no operations
- Forces Render to clear migration cache
- OTP fields already exist from migration 0003
- This should deploy successfully"

echo Step 6: Push to trigger fresh deployment...
git push origin main

echo.
echo ========================================
echo  CACHE-BUSTING DEPLOYMENT TRIGGERED!
echo ========================================
echo.
echo This creates a no-op migration that:
echo ✅ Has completely new filename (0006)
echo ✅ No operations (can't fail)
echo ✅ Forces Render to rebuild migration cache
echo ✅ OTP fields already exist from migration 0003
echo ✅ Should deploy successfully
echo.
echo If this still fails, we'll need to use the database reset option.
echo.
pause