@echo off
echo 🚀 Deploying Enhanced Reporting System
echo ========================================

echo 📊 Adding enhanced reporting files...
git add applications/reports_service.py
git add applications/views.py
git add applications/urls.py
git add templates/applications/admin_reports.html
git add templates/applications/officer_dashboard.html
git add templates/applications/officer_summary_report.html
git add templates/applications/officer_applications_report.html
git add deploy_enhanced_reports.bat

echo 💾 Committing changes...
git commit -m "Feature: Enhanced Reporting System for Admin and Officer Dashboards

🎯 New Features:
- Comprehensive ReportsService with advanced analytics
- Officer Dashboard with limited reporting capabilities
- Enhanced Summary Reports with processing time analysis
- Detailed Reports with advanced filtering
- Exception Reports with severity levels and recommendations
- Performance metrics and trend analysis

📊 Report Types Added:
- Summary Report: Overview statistics, trends, and key metrics
- Detailed Report: Complete application data with filtering
- Exception Report: Applications requiring attention
- Performance Report: Processing efficiency and trends

👥 User Roles:
- Admin: Full access to all reports and sensitive data
- Officer: Limited access to basic reports and statistics

🛠️ Technical Improvements:
- Centralized reporting logic in ReportsService
- Enhanced CSV export functionality
- Improved error handling and data validation
- Responsive design for all report templates
- Real-time statistics and trend analysis

📈 Analytics Features:
- Monthly application trends
- Processing time analysis
- District-wise statistics
- Gender distribution analysis
- Application type breakdown
- Exception monitoring with severity levels

🎉 Result: Comprehensive reporting system for better decision making and system monitoring"

echo 🌐 Pushing to GitHub main branch...
git push origin main

echo ✅ Enhanced Reporting System Successfully Deployed!
echo 📊 Features now available:
echo    - Admin Dashboard: Full reporting capabilities
echo    - Officer Dashboard: Limited reporting access
echo    - Summary Reports: Statistics and trends
echo    - Detailed Reports: Filterable application data
echo    - Exception Reports: Issue identification
echo    - CSV Export: All report types
echo    - Performance Metrics: System efficiency tracking
echo.
echo 🔍 Access URLs:
echo    - Admin Reports: /dashboard/reports/
echo    - Officer Dashboard: /officer-dashboard/
echo    - Officer Reports: /officer-reports/summary/
echo.
echo 🎉 Deployment Complete!
pause