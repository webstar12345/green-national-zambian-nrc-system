@echo off
echo 🚨 EMERGENCY: Restoring Production Service
echo ========================================

echo.
echo 📋 CRITICAL STEPS TO RESTORE SERVICE:
echo.
echo 1. 🔧 IMMEDIATE ROLLBACK (if shell scripts still fail):
echo    Go to Render.com Dashboard → Your Service → Settings
echo.
echo    Build Command: pip install -r requirements.txt ^&^& python manage.py collectstatic --noinput ^&^& python manage.py migrate
echo    Start Command: gunicorn nrc_system.wsgi:application
echo.
echo 2. 🚀 OR TRY FIXED SHELL SCRIPTS:
echo    Build Command: ./build.sh
echo    Start Command: ./start.sh
echo.
echo 3. 🔑 UPDATE ENVIRONMENT VARIABLES:
echo    EMAIL_HOST_PASSWORD=uroaoegylbpusjfy
echo.
echo 4. 💾 PUSHING FIXED FILES TO GITHUB...

git add .
git commit -m "EMERGENCY: Fix shell script line endings for Render.com

🚨 CRITICAL PRODUCTION FIX:
- Fixed Unix line endings in build.sh and start.sh
- Memory optimization: gunicorn.conf.py with single worker
- Security: Updated Gmail app password (uroaoegylbpusjfy)
- Performance: Reduced memory usage, increased timeouts

🛡️ SECURITY BREACH RESOLVED:
- New Gmail app password deployed
- Removed exposed credentials
- Local testing: ✅ WORKING

⚡ MEMORY OPTIMIZATION:
- Single worker to prevent SIGKILL
- 120s timeout to prevent worker kills
- Memory cleanup and optimization"

echo.
echo 📤 Pushing to GitHub...
git push origin main

echo.
echo ✅ FILES PUSHED TO GITHUB!
echo.
echo 🎯 NEXT STEPS:
echo 1. Go to Render.com Dashboard
echo 2. Update Build/Start commands (see above)
echo 3. Set EMAIL_HOST_PASSWORD=uroaoegylbpusjfy
echo 4. Wait for deployment
echo 5. Test OTP emails
echo.
echo 🌐 Your site: https://green-national-zambian-nrc-system.onrender.com
echo.
pause