@echo off
echo ========================================
echo  RENDER DEPLOYMENT GUIDE
echo ========================================
echo.

echo If your production site is on Render.com, follow these steps:
echo.

echo Step 1: Create deployment files...
mkdir render_deploy 2>nul

echo Step 2: Copy essential files...
copy applications\views.py render_deploy\ 2>nul
copy applications\ai_assistant.py render_deploy\ 2>nul
copy applications\models.py render_deploy\ 2>nul

echo Step 3: Create Render deployment guide...
echo # Render Deployment Guide for AI Assistant > render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo ## Method 1: GitHub Alternative (Recommended) >> render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo Since GitHub push is blocked, use one of these methods: >> render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo ### Option A: Manual File Upload >> render_deploy\RENDER_DEPLOY.md
echo 1. Go to your Render dashboard >> render_deploy\RENDER_DEPLOY.md
echo 2. Open your service settings >> render_deploy\RENDER_DEPLOY.md
echo 3. Use "Manual Deploy" option >> render_deploy\RENDER_DEPLOY.md
echo 4. Upload the changed files directly >> render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo ### Option B: New GitHub Repository >> render_deploy\RENDER_DEPLOY.md
echo 1. Create a new GitHub repository >> render_deploy\RENDER_DEPLOY.md
echo 2. Upload your files to the new repo >> render_deploy\RENDER_DEPLOY.md
echo 3. Connect Render to the new repository >> render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo ### Option C: Use GitHub Web Interface >> render_deploy\RENDER_DEPLOY.md
echo 1. Go to GitHub.com in your browser >> render_deploy\RENDER_DEPLOY.md
echo 2. Navigate to your repository >> render_deploy\RENDER_DEPLOY.md
echo 3. Upload files directly through web interface >> render_deploy\RENDER_DEPLOY.md
echo 4. Commit changes through browser >> render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo ## Environment Variables to Add: >> render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo In Render dashboard, add: >> render_deploy\RENDER_DEPLOY.md
echo GEMINI_API_KEY = your_actual_api_key >> render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo ## After Deployment: >> render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo Render will automatically: >> render_deploy\RENDER_DEPLOY.md
echo 1. Install requirements >> render_deploy\RENDER_DEPLOY.md
echo 2. Run migrations >> render_deploy\RENDER_DEPLOY.md
echo 3. Collect static files >> render_deploy\RENDER_DEPLOY.md
echo 4. Start the server >> render_deploy\RENDER_DEPLOY.md
echo. >> render_deploy\RENDER_DEPLOY.md
echo Your AI assistant will be live! >> render_deploy\RENDER_DEPLOY.md

echo.
echo ========================================
echo  RENDER GUIDE CREATED!
echo ========================================
echo.
echo Check render_deploy\RENDER_DEPLOY.md for detailed instructions
echo.
echo Quick options for Render deployment:
echo 1. Manual deploy through Render dashboard
echo 2. Create new GitHub repo and connect
echo 3. Upload files through GitHub web interface
echo.
pause