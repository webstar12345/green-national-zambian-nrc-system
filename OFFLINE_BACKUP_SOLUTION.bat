@echo off
echo ========================================
echo  OFFLINE BACKUP - Tomorrow Ready
echo ========================================
echo.

echo Creating backup for tomorrow's submission...
echo.

echo Step 1: Create submission folder...
mkdir submission_backup 2>nul

echo Step 2: Copy all essential files...
xcopy applications submission_backup\applications\ /E /I /Y
xcopy accounts submission_backup\accounts\ /E /I /Y
xcopy nrc_system submission_backup\nrc_system\ /E /I /Y
xcopy templates submission_backup\templates\ /E /I /Y
xcopy static submission_backup\static\ /E /I /Y
copy manage.py submission_backup\ 2>nul
copy requirements.txt submission_backup\ 2>nul
copy .env.example submission_backup\ 2>nul
copy AI_ASSISTANT_RESTORED.md submission_backup\ 2>nul
copy DATABASE_TABLES_COMPLETE.md submission_backup\ 2>nul
copy db.sqlite3 submission_backup\ 2>nul

echo Step 3: Create README for submission...
echo # Zambian NRC System with AI Assistant > submission_backup\README_SUBMISSION.txt
echo. >> submission_backup\README_SUBMISSION.txt
echo This system includes: >> submission_backup\README_SUBMISSION.txt
echo - Multilingual AI Assistant (English, Bemba, Nyanja, Tonga, Lozi) >> submission_backup\README_SUBMISSION.txt
echo - Complete NRC application processing >> submission_backup\README_SUBMISSION.txt
echo - Database migrations applied >> submission_backup\README_SUBMISSION.txt
echo - User authentication and authorization >> submission_backup\README_SUBMISSION.txt
echo - Responsive web interface >> submission_backup\README_SUBMISSION.txt
echo. >> submission_backup\README_SUBMISSION.txt
echo To run: >> submission_backup\README_SUBMISSION.txt
echo 1. pip install -r requirements.txt >> submission_backup\README_SUBMISSION.txt
echo 2. python manage.py migrate >> submission_backup\README_SUBMISSION.txt
echo 3. python manage.py runserver >> submission_backup\README_SUBMISSION.txt
echo. >> submission_backup\README_SUBMISSION.txt
echo AI Assistant is fully functional with fallback responses. >> submission_backup\README_SUBMISSION.txt

echo Step 4: Create ZIP for easy submission...
powershell Compress-Archive -Path submission_backup\* -DestinationPath NRC_System_AI_Assistant_Final.zip -Force

echo.
echo ========================================
echo  BACKUP COMPLETE!
echo ========================================
echo.
echo Created:
echo 1. submission_backup\ folder with all files
echo 2. NRC_System_AI_Assistant_Final.zip
echo.
echo For tomorrow's submission, you have:
echo - Complete working system
echo - AI Assistant (5 languages)
echo - All documentation
echo - Ready to run locally
echo.
echo Even without GitHub, you're ready!
echo.
pause