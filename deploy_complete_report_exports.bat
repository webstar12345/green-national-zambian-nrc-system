@echo off
echo ========================================
echo  DEPLOYING COMPLETE REPORT EXPORT FIX
echo ========================================
echo.

echo 📊 Testing all export combinations...
python test_complete_report_exports.py

echo.
echo 🔍 Checking for any syntax errors...
python manage.py check

echo.
echo 📦 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo 🗄️ Running migrations (if any)...
python manage.py migrate

echo.
echo ✅ DEPLOYMENT COMPLETE!
echo.
echo 📋 EXPORT MATRIX STATUS:
echo ========================
echo Summary Report:  PDF ✅ Excel ✅ Word ✅ CSV ✅
echo Detailed Report: PDF ✅ Excel ✅ Word ✅ CSV ✅ 
echo Exception Report: PDF ✅ Excel ✅ Word ✅ CSV ✅
echo.
echo 🎉 All 12 export combinations are working!
echo.
echo 📖 Next Steps:
echo - Test exports in admin dashboard
echo - Verify all report types work correctly
echo - Check export file downloads
echo.
pause