@echo off
echo ========================================
echo   DEPLOYING ENHANCED PDF REPORTS
echo ========================================
echo.

echo 📊 Enhanced PDF Report System Deployment
echo.
echo Key Features:
echo • Professional PDF reports with Zambian branding
echo • Removed Word and Excel dependencies
echo • Enhanced structure and formatting
echo • Status-based color coding
echo • Comprehensive exception reporting
echo.

echo 🔧 Step 1: Testing report structure...
python test_enhanced_pdf_reports.py
if errorlevel 1 (
    echo ❌ Report tests failed!
    pause
    exit /b 1
)

echo.
echo ✅ Step 2: Collecting static files...
python manage.py collectstatic --noinput

echo.
echo 🔄 Step 3: Running migrations (if needed)...
python manage.py migrate --noinput

echo.
echo 🧹 Step 4: Clearing cache...
python clear_cache.py

echo.
echo 📋 Step 5: Checking system status...
python manage.py check --deploy

echo.
echo ========================================
echo   DEPLOYMENT SUMMARY
echo ========================================
echo.
echo ✅ Enhanced PDF Reports Deployed Successfully!
echo.
echo New Features:
echo • PDF-only professional reports
echo • Zambian color scheme (Green, Orange, Red)
echo • Enhanced data visualization
echo • Better exception reporting
echo • Removed unnecessary dependencies
echo.
echo Report Types Available:
echo • Summary Report - Executive overview with statistics
echo • Detailed Report - Complete application data
echo • Exception Report - Issues requiring attention
echo.
echo Export Formats:
echo • PDF - Professional formatted reports
echo • CSV - Raw data for analysis
echo.
echo 🌐 Access reports at: /admin/reports/
echo.
echo ========================================
pause