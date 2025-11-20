@echo off
echo Pushing Gemini API setup guides...
git add GEMINI_API_SETUP.md
git add QUICK_GEMINI_SETUP.txt
git add applications/ai_assistant.py
git commit -m "Add Gemini API setup guides and fallback system"
git push
echo.
echo ========================================
echo GEMINI API GUIDES ADDED!
echo ========================================
echo.
echo Files created:
echo - GEMINI_API_SETUP.md (detailed guide)
echo - QUICK_GEMINI_SETUP.txt (quick reference)
echo.
echo Next steps:
echo 1. Get API key from: https://aistudio.google.com/app/apikey
echo 2. Add to Render environment variables
echo 3. Wait for deployment
echo 4. Test the AI assistant!
echo.
echo ========================================
pause
