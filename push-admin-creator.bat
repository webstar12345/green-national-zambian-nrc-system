@echo off
echo Pushing automatic admin creator...
git add accounts/management/
git add build.sh
git commit -m "Add automatic admin account creation on deployment"
git push
echo.
echo Done! After deployment, you can login with:
echo Username: admin
echo Password: ChangeMe123!
echo.
echo IMPORTANT: Change the password after first login!
pause
