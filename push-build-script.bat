@echo off
echo Pushing build script to GitHub...
git add build.sh
git commit -m "Add build script for Render deployment"
git push
echo.
echo Done! Now update Build Command on Render to: ./build.sh
pause
