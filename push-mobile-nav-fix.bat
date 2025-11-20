@echo off
echo Pushing improved mobile navigation...
git add templates/base.html
git add static/css/mobile-responsive.css
git add accounts/management/commands/createdefaultadmin.py
git commit -m "Enhance mobile navigation with better styling and UX"
git push
echo.
echo ========================================
echo MOBILE NAVIGATION IMPROVED!
echo ========================================
echo.
echo Changes:
echo - Better mobile menu styling
echo - Smooth animations
echo - Larger touch targets
echo - Auto-close on link click
echo - Visual feedback on hover
echo - Gradient background
echo - Icon animations
echo.
echo Test on your mobile device!
echo ========================================
pause
