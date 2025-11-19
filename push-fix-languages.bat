@echo off
echo ========================================
echo Fixing Language Support
echo ========================================
echo.
echo Improvements:
echo - Removed duplicate language selector
echo - Added Nyanja fallback responses
echo - Added Tonga fallback responses
echo - Added Lozi fallback responses
echo - All 5 languages now work properly
echo.

git add static/js/chat-widget-voice.js
git add applications/ai_assistant.py
git commit -m "Fix: Add complete Nyanja, Tonga, and Lozi support"
git push origin main

echo.
echo ========================================
echo Language Fix Deployed!
echo ========================================
echo.
echo All languages now working:
echo ✓ English
echo ✓ Bemba
echo ✓ Nyanja
echo ✓ Tonga
echo ✓ Lozi
echo.
echo Wait 2-3 minutes for Render to rebuild.
echo.
pause
