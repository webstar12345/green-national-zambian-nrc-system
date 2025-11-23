@echo off
echo ========================================
echo  Deploying Auth Page Redesign
echo ========================================
echo.

echo Adding files to git...
git add templates/accounts/login.html
git add templates/accounts/signup.html
git add setup_new_oauth.bat
git add push-auth-redesign.bat

echo.
echo Committing changes...
git commit -m "Redesign login and signup pages with modern gradient UI"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo  Deployment Complete!
echo ========================================
echo.
echo Your new auth pages are now live with:
echo - Modern gradient backgrounds
echo - Professional card-based design
echo - Better visual hierarchy
echo - Improved user experience
echo.
pause
