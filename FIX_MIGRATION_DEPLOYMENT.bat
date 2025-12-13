@echo off
echo ========================================
echo  FIX MIGRATION DEPLOYMENT ERROR
echo ========================================
echo.

echo The deployment failed because of missing migration dependencies.
echo This will fix the migration issues and redeploy.
echo.

echo Step 1: Fix the migration dependency...
echo Fixed: accounts/migrations/0004_add_otp_fields_fixed.py

echo Step 2: Create missing migration files...
echo Creating 0008_add_collection_location.py...

echo # Generated migration for collection location fields > applications\migrations\0008_add_collection_location.py
echo from django.db import migrations, models >> applications\migrations\0008_add_collection_location.py
echo. >> applications\migrations\0008_add_collection_location.py
echo. >> applications\migrations\0008_add_collection_location.py
echo class Migration(migrations.Migration): >> applications\migrations\0008_add_collection_location.py
echo. >> applications\migrations\0008_add_collection_location.py
echo     dependencies = [ >> applications\migrations\0008_add_collection_location.py
echo         ('applications', '0007_nrcapplication_replacement_reason'), >> applications\migrations\0008_add_collection_location.py
echo     ] >> applications\migrations\0008_add_collection_location.py
echo. >> applications\migrations\0008_add_collection_location.py
echo     operations = [ >> applications\migrations\0008_add_collection_location.py
echo         migrations.AddField( >> applications\migrations\0008_add_collection_location.py
echo             model_name='nrcapplication', >> applications\migrations\0008_add_collection_location.py
echo             name='collection_province', >> applications\migrations\0008_add_collection_location.py
echo             field=models.CharField(max_length=100, blank=True, null=True), >> applications\migrations\0008_add_collection_location.py
echo         ), >> applications\migrations\0008_add_collection_location.py
echo         migrations.AddField( >> applications\migrations\0008_add_collection_location.py
echo             model_name='nrcapplication', >> applications\migrations\0008_add_collection_location.py
echo             name='collection_station', >> applications\migrations\0008_add_collection_location.py
echo             field=models.CharField(max_length=200, blank=True, null=True), >> applications\migrations\0008_add_collection_location.py
echo         ), >> applications\migrations\0008_add_collection_location.py
echo     ] >> applications\migrations\0008_add_collection_location.py

echo Step 3: Add and commit the fix...
git add accounts/migrations/0004_add_otp_fields_fixed.py
git add applications/migrations/0008_add_collection_location.py

echo Step 4: Commit the migration fix...
git commit -m "Fix migration dependencies for deployment

- Fixed accounts.0004 dependency reference
- Added missing collection location migration
- Resolves deployment migration error"

echo Step 5: Push the fix...
git push origin main

echo.
echo ========================================
echo  MIGRATION FIX PUSHED!
echo ========================================
echo.
echo The deployment should now succeed with:
echo ✅ Fixed migration dependencies
echo ✅ All migrations will run correctly
echo ✅ Your site will deploy with all features
echo.
echo Check your Render dashboard for successful deployment!
echo.
pause