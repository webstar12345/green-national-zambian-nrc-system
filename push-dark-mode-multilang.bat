@echo off
echo ========================================
echo Deploying Dark Mode and Multilingual AI
echo ========================================
echo.
echo New Features:
echo - Dark Mode toggle (moon/sun icon)
echo - AI Assistant in Nyanja, Tonga, Lozi
echo - Language selector in chat widget
echo - Accurate translations for all languages
echo.

git add static/css/dark-mode.css
git add static/js/dark-mode.js
git add static/css/chat-widget-voice.css
git add static/js/chat-widget-voice.js
git add applications/ai_assistant.py
git add applications/views.py
git add templates/base.html
git commit -m "Add dark mode and multilingual AI support (Nyanja, Tonga, Lozi)"
git push origin main

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Features Added:
echo ✓ Dark mode with floating toggle button
echo ✓ AI responses in Nyanja, Tonga, and Lozi
echo ✓ Language selector in chat widget
echo ✓ Persistent theme and language preferences
echo.
echo Wait 2-3 minutes for Render to rebuild.
echo.
pause
