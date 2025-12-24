@echo off
echo ========================================
echo   DEPLOYING CENTERED REPORT HEADERS
echo ========================================
echo.

echo 🎯 Centered Header Alignment Update
echo.
echo Changes Made:
echo • Section headers now centered above tables
echo • Subsection headers centered for better organization
echo • Table data aligned to center for better readability
echo • Consistent alignment throughout all report types
echo.

echo 🔧 Step 1: Testing centered header alignment...
python test_centered_report_headers.py
if errorlevel 1 (
    echo ❌ Header alignment tests failed!
    pause
    exit /b 1
)

echo.
echo ✅ Step 2: Testing full report generation...
python test_enhanced_pdf_reports.py
if errorlevel 1 (
    echo ❌ Full report tests failed!
    pause
    exit /b 1
)

echo.
echo 🔄 Step 3: Clearing cache...
python clear_cache.py

echo.
echo ========================================
echo   DEPLOYMENT SUMMARY
echo ========================================
echo.
echo ✅ Centered Report Headers Deployed Successfully!
echo.
echo Updated Alignments:
echo • Main Report Title: CENTERED
echo • Section Headers: CENTERED (above each table)
echo • Subsection Headers: CENTERED
echo • Table Headers: CENTERED
echo • Table Data: CENTERED
echo.
echo Report Types Updated:
echo • Summary Report - All headers centered
echo • Detailed Report - All headers centered
echo • Exception Report - All headers centered
echo.
echo Visual Improvements:
echo • Better visual hierarchy
echo • More professional appearance
echo • Consistent alignment throughout
echo • Enhanced readability
echo.
echo 🌐 Test the updated reports at: /admin/reports/
echo.
echo ========================================
pause