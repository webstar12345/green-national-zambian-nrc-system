@echo off
echo ========================================
echo  QUICK PUSH TO MAIN
echo ========================================
echo.

echo Pushing cache fix to main branch for Render deployment...
echo.

git push origin all-features-final
git checkout main
git merge all-features-final
git push origin main

echo.
echo DONE! Check Render dashboard for deployment.
echo.
pause