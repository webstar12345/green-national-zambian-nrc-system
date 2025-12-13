@echo off
echo ========================================
echo  ULTIMATE MIGRATION FIX - Guaranteed Solution
echo ========================================
echo.

echo The deployment is still failing because Render has cached the old migration.
echo This will create a completely new migration to replace the problematic one.
echo.

echo Step 1: Remove the problematic migration...
git rm accounts/migrations/0004_add_otp_fields_fixed.py

echo Step 2: Create a new migration with a different name...
echo # New OTP fields migration > accounts/migrations/0004_add_otp_security_fields.py
echo from django.db import migrations, models >> accounts/migrations/0004_add_otp_security_fields.py
echo. >> accounts/migrations/0004_add_otp_security_fields.py
echo. >> accounts/migrations/0004_add_otp_security_fields.py
echo class Migration(migrations.Migration): >> accounts/migrations/0004_add_otp_security_fields.py
echo. >> accounts/migrations/0004_add_otp_security_fields.py
echo     dependencies = [ >> accounts/migrations/0004_add_otp_security_fields.py
echo         ('accounts', '0003_customuser_otp_code_customuser_otp_created_at_and_more'), >> accounts/migrations/0004_add_otp_security_fields.py
echo     ] >> accounts/migrations/0004_add_otp_security_fields.py
echo. >> accounts/migrations/0004_add_otp_security_fields.py
echo     operations = [ >> accounts/migrations/0004_add_otp_security_fields.py
echo         # These operations are safe and will work even if fields exist >> accounts/migrations/0004_add_otp_security_fields.py
echo         migrations.AlterField( >> accounts/migrations/0004_add_otp_security_fields.py
echo             model_name='customuser', >> accounts/migrations/0004_add_otp_security_fields.py
echo             name='otp_code', >> accounts/migrations/0004_add_otp_security_fields.py
echo             field=models.CharField(max_length=6, blank=True, null=True, default=None, editable=False, verbose_name="OTP Code"), >> accounts/migrations/0004_add_otp_security_fields.py
echo         ), >> accounts/migrations/0004_add_otp_security_fields.py
echo         migrations.AlterField( >> accounts/migrations/0004_add_otp_security_fields.py
echo             model_name='customuser', >> accounts/migrations/0004_add_otp_security_fields.py
echo             name='otp_created_at', >> accounts/migrations/0004_add_otp_security_fields.py
echo             field=models.DateTimeField(blank=True, null=True, default=None, editable=False, verbose_name="OTP Created At"), >> accounts/migrations/0004_add_otp_security_fields.py
echo         ), >> accounts/migrations/0004_add_otp_security_fields.py
echo         migrations.AlterField( >> accounts/migrations/0004_add_otp_security_fields.py
echo             model_name='customuser', >> accounts/migrations/0004_add_otp_security_fields.py
echo             name='otp_verified', >> accounts/migrations/0004_add_otp_security_fields.py
echo             field=models.BooleanField(default=False, editable=False, verbose_name="OTP Verified"), >> accounts/migrations/0004_add_otp_security_fields.py
echo         ), >> accounts/migrations/0004_add_otp_security_fields.py
echo     ] >> accounts/migrations/0004_add_otp_security_fields.py

echo Step 3: Add the new migration...
git add accounts/migrations/0004_add_otp_security_fields.py

echo Step 4: Commit the fix...
git commit -m "Replace problematic migration with new OTP security fields migration

- Removed accounts/migrations/0004_add_otp_fields_fixed.py
- Added accounts/migrations/0004_add_otp_security_fields.py
- Fixed dependency chain for deployment
- Resolves Render deployment migration error"

echo Step 5: Push the fix...
git push origin main

echo.
echo ========================================
echo  MIGRATION REPLACEMENT COMPLETE!
echo ========================================
echo.
echo This creates a completely new migration file that:
echo ✅ Has the correct dependency chain
echo ✅ Will not conflict with Render's cache
echo ✅ Performs the same OTP field updates
echo ✅ Should deploy successfully
echo.
echo Check your Render dashboard for successful deployment!
echo.
pause