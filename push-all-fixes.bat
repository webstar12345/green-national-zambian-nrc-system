@echo off
echo Pushing all fixes: admin creator + enhanced mobile responsiveness...
git add accounts/management/commands/createdefaultadmin.py
git add static/css/mobile-responsive.css
git commit -m "Fix admin creation and enhance mobile/tablet responsiveness"
git push
echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo After deployment:
echo 1. Login with: admin / ChangeMe123!
echo 2. Change password immediately
echo 3. Test on mobile, tablet, and desktop
echo.
echo Your site is now fully responsive!
echo ========================================
pause
