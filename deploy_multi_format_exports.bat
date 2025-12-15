@echo off
echo 🚀 Deploying Multi-Format Report Export System
echo ========================================

echo 📦 Installing required packages...
pip install reportlab==4.0.7 openpyxl==3.1.2 python-docx==1.1.0 xlsxwriter==3.1.9

echo 📊 Adding multi-format export files...
git add requirements.txt
git add applications/report_exporters.py
git add applications/reports_service.py
git add applications/views.py
git add templates/applications/admin_reports.html
git add templates/applications/summary_report.html
git add templates/applications/detailed_report.html
git add templates/applications/exception_report.html
git add deploy_multi_format_exports.bat

echo 💾 Committing changes...
git commit -m "Feature: Multi-Format Report Export System (PDF, Excel, Word)

🎯 New Export Formats:
- PDF Export: Professional formatted reports with tables and styling
- Excel Export: Spreadsheet format with multiple sheets and formatting
- Word Export: Document format with tables and professional layout
- CSV Export: Enhanced with better formatting (existing)

📊 Export Features:
- Summary Reports: Statistics and charts in all formats
- Detailed Reports: Complete application data with formatting
- Exception Reports: Issue tracking with color-coded severity
- Professional styling and branding for all formats

🛠️ Technical Implementation:
- ReportLab for PDF generation with charts and styling
- OpenPyXL for Excel files with formatting and multiple sheets
- Python-docx for Word documents with tables
- Enhanced export service with format detection
- Dropdown export menus in all report templates

📈 Export Capabilities:
- PDF: Professional reports with Zambian branding
- Excel: Multi-sheet workbooks with charts and formatting
- Word: Structured documents with tables and styling
- All formats maintain data integrity and professional appearance

🎨 UI Improvements:
- Export dropdown menus on all report pages
- Format-specific icons and styling
- Quick export buttons on main reports page
- Responsive design for all export options

🎉 Result: Complete multi-format reporting system for professional document generation"

echo 🌐 Pushing to GitHub main branch...
git push origin main

echo ✅ Multi-Format Export System Successfully Deployed!
echo 📊 Available Export Formats:
echo    - PDF: Professional formatted reports
echo    - Excel: Spreadsheet with charts and formatting  
echo    - Word: Document format with tables
echo    - CSV: Enhanced comma-separated values
echo.
echo 🔍 Export Options Available On:
echo    - Summary Reports: All statistics and trends
echo    - Detailed Reports: Complete application data
echo    - Exception Reports: Issue tracking and analysis
echo    - Admin Dashboard: Quick export buttons
echo.
echo 📦 Required Packages Installed:
echo    - reportlab: PDF generation
echo    - openpyxl: Excel file creation
echo    - python-docx: Word document generation
echo    - xlsxwriter: Advanced Excel features
echo.
echo 🎉 Deployment Complete!
pause