@echo off
echo Pushing Voice-Enabled AI Assistant...
git add static/js/chat-widget-voice.js
git add static/css/chat-widget-voice.css
git add templates/base.html
git add VOICE_ASSISTANT_GUIDE.md
git add applications/views.py
git add applications/urls.py
git add templates/applications/about.html
git add templates/applications/services.html
git add accounts/management/
git add static/css/mobile-responsive.css
git commit -m "Add voice input/output to AI assistant with About and Services pages"
git push
echo.
echo ========================================
echo VOICE AI ASSISTANT DEPLOYED!
echo ========================================
echo.
echo New Features:
echo - Voice Input (Speech-to-Text)
echo - Voice Output (Text-to-Speech)
echo - Microphone button for voice input
echo - Speaker toggle for voice responses
echo - Visual recording indicators
echo - Multi-language support
echo - Mobile-friendly voice controls
echo.
echo Also Added:
echo - About Us page with team section
echo - Services page with detailed info
echo - Enhanced mobile navigation
echo - Admin auto-creation on deployment
echo.
echo Test voice features:
echo 1. Click microphone button
echo 2. Speak your question
echo 3. Toggle speaker for voice responses
echo.
echo Browser Support:
echo - Chrome/Edge: Full support
echo - Safari: Full support
echo - Firefox: Limited voice input
echo.
echo ========================================
pause
