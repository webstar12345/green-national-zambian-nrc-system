@echo off
echo ========================================
echo Deploying Cloudinary Image Storage Fix
echo ========================================
echo.
echo This fixes the disappearing profile images issue!
echo.
echo What this does:
echo - Adds Cloudinary for permanent image storage
echo - Profile images will never disappear again
echo - Images stored in cloud, not on server
echo - Faster loading with CDN
echo.

git add requirements.txt
git add nrc_system/settings.py
git add .env.example
git add CLOUDINARY_SETUP_GUIDE.md
git add push-cloudinary-fix.bat
git commit -m "Fix: Add Cloudinary for permanent image storage"
git push origin main

echo.
echo ========================================
echo Code Deployed!
echo ========================================
echo.
echo IMPORTANT: You must set up Cloudinary!
echo.
echo Next Steps:
echo 1. Create FREE Cloudinary account at: https://cloudinary.com/users/register/free
echo 2. Get your credentials (Cloud Name, API Key, API Secret)
echo 3. Add 4 environment variables to Render:
echo    - USE_CLOUDINARY=True
echo    - CLOUDINARY_CLOUD_NAME=your-cloud-name
echo    - CLOUDINARY_API_KEY=your-api-key
echo    - CLOUDINARY_API_SECRET=your-api-secret
echo 4. Render will auto-rebuild
echo 5. Test profile image upload
echo.
echo Read CLOUDINARY_SETUP_GUIDE.md for detailed instructions!
echo.
pause
