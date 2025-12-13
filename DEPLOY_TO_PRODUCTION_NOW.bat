@echo off
echo ========================================
echo  DEPLOY AI ASSISTANT TO PRODUCTION
echo ========================================
echo.

echo This will help you deploy your new AI assistant to production
echo.

echo Step 1: Create deployment package...
mkdir production_deploy 2>nul

echo Step 2: Copy only the changed AI assistant files...
copy applications\views.py production_deploy\ 2>nul
copy applications\ai_assistant.py production_deploy\ 2>nul
copy applications\models.py production_deploy\ 2>nul
copy applications\migrations\0009_create_separate_nrc_tables.py production_deploy\ 2>nul
copy applications\migrations\0010_migrate_existing_data.py production_deploy\ 2>nul

echo Step 3: Copy static files for AI assistant...
mkdir production_deploy\static 2>nul
mkdir production_deploy\static\js 2>nul
mkdir production_deploy\static\css 2>nul
copy static\js\chat-widget.js production_deploy\static\js\ 2>nul
copy static\css\chat-widget.css production_deploy\static\css\ 2>nul

echo Step 4: Copy AI demo template...
mkdir production_deploy\templates 2>nul
mkdir production_deploy\templates\applications 2>nul
copy templates\applications\ai_demo.html production_deploy\templates\applications\ 2>nul

echo Step 5: Create deployment instructions...
echo # AI Assistant Deployment Instructions > production_deploy\DEPLOY_INSTRUCTIONS.md
echo. >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo ## Files to Upload to Production: >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo. >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 1. applications/views.py - Contains restored AI functions >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 2. applications/ai_assistant.py - AI assistant core functionality >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 3. applications/models.py - Updated database models >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 4. applications/migrations/0009_create_separate_nrc_tables.py >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 5. applications/migrations/0010_migrate_existing_data.py >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 6. static/js/chat-widget.js - AI chat interface >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 7. static/css/chat-widget.css - AI chat styling >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 8. templates/applications/ai_demo.html - AI demo page >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo. >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo ## Environment Variables Needed: >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo. >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo Add to your production environment: >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo GEMINI_API_KEY=your_gemini_api_key_here >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo. >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo ## After Upload: >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo. >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 1. Run migrations: python manage.py migrate >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 2. Collect static files: python manage.py collectstatic >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo 3. Restart your production server >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo. >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo ## AI Assistant Features: >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo. >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo - Multilingual support (English, Bemba, Nyanja, Tonga, Lozi) >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo - Smart NRC guidance with context-aware responses >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo - Fallback system when API quota exceeded >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo - Quick response suggestions >> production_deploy\DEPLOY_INSTRUCTIONS.md
echo - Session-based language preferences >> production_deploy\DEPLOY_INSTRUCTIONS.md

echo Step 6: Create ZIP for easy upload...
powershell Compress-Archive -Path production_deploy\* -DestinationPath AI_Assistant_Production_Update.zip -Force

echo.
echo ========================================
echo  PRODUCTION PACKAGE READY!
echo ========================================
echo.
echo Created:
echo 1. production_deploy\ folder with changed files
echo 2. AI_Assistant_Production_Update.zip
echo 3. DEPLOY_INSTRUCTIONS.md with step-by-step guide
echo.
echo To deploy to production:
echo 1. Upload the files to your production server
echo 2. Add GEMINI_API_KEY environment variable
echo 3. Run migrations and collect static files
echo 4. Restart server
echo.
echo Your live site will then have the AI assistant!
echo.
pause