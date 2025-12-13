@echo off
echo 🚨 QUICK RENDER DEPLOYMENT FIX
echo ================================
echo.
echo This will remove the problematic migration files to fix Render deployment
echo.
pause

echo 🗑️  Removing problematic migration files...
if exist "applications\migrations\0008_create_separate_nrc_tables.py" (
    del "applications\migrations\0008_create_separate_nrc_tables.py"
    echo ✅ Removed 0008_create_separate_nrc_tables.py
) else (
    echo ⚠️  0008_create_separate_nrc_tables.py not found
)

if exist "applications\migrations\0009_migrate_existing_data.py" (
    del "applications\migrations\0009_migrate_existing_data.py"
    echo ✅ Removed 0009_migrate_existing_data.py
) else (
    echo ⚠️  0009_migrate_existing_data.py not found
)

echo.
echo 📝 Committing changes...
git add .
git commit -m "Fix Render deployment - remove NRC separation migrations"

echo.
echo 🚀 Pushing to main branch...
git push origin main

echo.
echo ✅ DEPLOYMENT FIX COMPLETE!
echo.
echo 📋 What happened:
echo - Removed problematic migration files
echo - Committed changes to git
echo - Pushed to main branch for Render deployment
echo.
echo 🔄 Next steps:
echo 1. Wait for Render deployment to succeed
echo 2. Check Render migration state
echo 3. Re-implement table separation with correct dependencies
echo.
pause