@echo off
echo ========================================
echo  GITHUB WEB UPLOAD - ALL FEATURES
echo ========================================
echo.

echo Creating organized folders for GitHub web upload...
echo.

echo Step 1: Create upload folders...
mkdir github_upload 2>nul
mkdir github_upload\applications 2>nul
mkdir github_upload\accounts 2>nul
mkdir github_upload\templates 2>nul
mkdir github_upload\static 2>nul

echo Step 2: Copy core application files...
xcopy applications\*.py github_upload\applications\ /Y
xcopy applications\migrations\*.py github_upload\applications\migrations\ /Y /I

echo Step 3: Copy account files...
xcopy accounts\*.py github_upload\accounts\ /Y
xcopy accounts\migrations\*.py github_upload\accounts\migrations\ /Y /I
xcopy accounts\management\commands\*.py github_upload\accounts\management\commands\ /Y /I

echo Step 4: Copy templates...
xcopy templates\*.html github_upload\templates\ /E /Y /I

echo Step 5: Copy static files...
xcopy static\css\*.css github_upload\static\css\ /Y /I
xcopy static\js\*.js github_upload\static\js\ /Y /I
xcopy static\manifest.json github_upload\static\ /Y
xcopy static\sw.js github_upload\static\ /Y

echo Step 6: Copy root files...
copy manage.py github_upload\ 2>nul
copy requirements.txt github_upload\ 2>nul
copy runtime.txt github_upload\ 2>nul
copy .env.example github_upload\ 2>nul
copy build.sh github_upload\ 2>nul

echo Step 7: Copy documentation...
copy AI_ASSISTANT_RESTORED.md github_upload\ 2>nul
copy DATABASE_TABLES_COMPLETE.md github_upload\ 2>nul
copy OTP_IMPLEMENTATION_SUMMARY.md github_upload\ 2>nul
copy PWA_SETUP_GUIDE.md github_upload\ 2>nul
copy COMPLETE_SYSTEM_SUMMARY.md github_upload\ 2>nul

echo Step 8: Create upload instructions...
echo # GitHub Web Upload Instructions > github_upload\UPLOAD_INSTRUCTIONS.md
echo. >> github_upload\UPLOAD_INSTRUCTIONS.md
echo ## Upload Order: >> github_upload\UPLOAD_INSTRUCTIONS.md
echo. >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 1. Upload root files first (manage.py, requirements.txt, etc.) >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 2. Upload applications folder >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 3. Upload accounts folder >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 4. Upload templates folder >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 5. Upload static folder >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 6. Upload documentation files >> github_upload\UPLOAD_INSTRUCTIONS.md
echo. >> github_upload\UPLOAD_INSTRUCTIONS.md
echo ## For Each Upload: >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 1. Go to GitHub.com repository >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 2. Click "Add file" - "Upload files" >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 3. Drag and drop files/folders >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 4. Add commit message describing the upload >> github_upload\UPLOAD_INSTRUCTIONS.md
echo 5. Click "Commit changes" >> github_upload\UPLOAD_INSTRUCTIONS.md
echo. >> github_upload\UPLOAD_INSTRUCTIONS.md
echo ## Features Being Uploaded: >> github_upload\UPLOAD_INSTRUCTIONS.md
echo - AI Assistant (5 languages) >> github_upload\UPLOAD_INSTRUCTIONS.md
echo - OTP Security System >> github_upload\UPLOAD_INSTRUCTIONS.md
echo - Enhanced Landing Page >> github_upload\UPLOAD_INSTRUCTIONS.md
echo - PWA Features >> github_upload\UPLOAD_INSTRUCTIONS.md
echo - Database Improvements >> github_upload\UPLOAD_INSTRUCTIONS.md
echo - Authentication Enhancements >> github_upload\UPLOAD_INSTRUCTIONS.md

echo Step 9: Create ZIP for bulk upload...
powershell Compress-Archive -Path github_upload\* -DestinationPath Complete_NRC_System_Upload.zip -Force

echo.
echo ========================================
echo  GITHUB UPLOAD PACKAGE READY!
echo ========================================
echo.
echo Created:
echo 1. github_upload\ folder - organized for web upload
echo 2. Complete_NRC_System_Upload.zip - for bulk upload
echo 3. UPLOAD_INSTRUCTIONS.md - step-by-step guide
echo.
echo To upload to GitHub:
echo 1. Go to your GitHub repository
echo 2. Use "Upload files" to add folders one by one
echo 3. Or extract ZIP and upload in batches
echo.
echo All your new features will be on GitHub!
echo.
pause