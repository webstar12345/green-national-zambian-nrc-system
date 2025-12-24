@echo off
echo ========================================
echo   EMERGENCY RENDER DATABASE FIX
echo ========================================
echo.

echo 🚨 CRITICAL: Database Connection Error
echo.
echo Error: [Errno -2] Name or service not known
echo This means your app cannot connect to PostgreSQL
echo.

echo 🔧 IMMEDIATE ACTION REQUIRED:
echo.
echo 1. Go to Render Dashboard: https://dashboard.render.com
echo 2. Navigate to your PostgreSQL service
echo 3. Copy the EXTERNAL Database URL (ends with -a)
echo 4. Go to your Web Service settings
echo 5. Update DATABASE_URL environment variable
echo 6. Save and wait for redeploy
echo.

echo 📋 Running diagnostic script...
python fix_render_database_connection.py

echo.
echo ========================================
echo   CRITICAL STEPS TO TAKE NOW
echo ========================================
echo.
echo □ 1. Open Render Dashboard
echo □ 2. Get External Database URL from PostgreSQL service
echo □ 3. Update DATABASE_URL in Web Service environment
echo □ 4. Ensure URL ends with '-a'
echo □ 5. Save changes and wait for redeploy
echo □ 6. Test application
echo.
echo 🔗 Dashboard: https://dashboard.render.com
echo 📖 Full Guide: See EMERGENCY_DATABASE_FIX.md
echo.
echo ⚠️  DO NOT IGNORE - Your app is DOWN until this is fixed!
echo.
pause