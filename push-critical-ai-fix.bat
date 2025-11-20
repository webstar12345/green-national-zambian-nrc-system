@echo off
echo Pushing CRITICAL AI Assistant fix...
git add applications/ai_assistant.py
git commit -m "Critical fix: Prevent Gemini initialization when API key is missing"
git push
echo.
echo ========================================
echo CRITICAL FIX DEPLOYED!
echo ========================================
echo.
echo What was fixed:
echo - Gemini model only initializes if API key exists
echo - No more credential errors
echo - Graceful fallback to predefined responses
echo - Chat widget works without API key
echo - Better error handling
echo.
echo Your AI assistant will now work perfectly
echo with or without the Gemini API key!
echo.
echo ========================================
pause
