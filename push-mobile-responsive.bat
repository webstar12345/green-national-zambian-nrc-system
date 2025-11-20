@echo off
echo Pushing mobile responsive updates to GitHub...
git add templates/base.html
git add static/css/mobile-responsive.css
git commit -m "Add mobile responsive design with hamburger menu"
git push
echo.
echo Done! Your site is now mobile responsive!
pause
