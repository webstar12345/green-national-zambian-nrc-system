@echo off
echo Pushing About Us and Services pages...
git add applications/views.py
git add applications/urls.py
git add templates/applications/about.html
git add templates/applications/services.html
git add templates/base.html
git add accounts/management/
git add static/css/mobile-responsive.css
git commit -m "Add About Us and Services pages with team section and mobile responsive design"
git push
echo.
echo ========================================
echo ABOUT US & SERVICES PAGES ADDED!
echo ========================================
echo.
echo New Pages:
echo - /about/ - About Us with team section
echo - /services/ - Our Services page
echo.
echo Features:
echo - Beautiful responsive design
echo - Team member cards
echo - Service descriptions
echo - FAQ section
echo - Statistics
echo - Call-to-action buttons
echo.
echo Navigation updated on desktop and mobile!
echo ========================================
pause
