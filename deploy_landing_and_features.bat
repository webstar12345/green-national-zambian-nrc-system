@echo off
echo 🚀 DEPLOYING LANDING PAGE AND ALL FEATURES
echo ==========================================
echo.
echo This will deploy:
echo ✅ Public landing page (no login required)
echo ✅ OTP verification system
echo ✅ Dark mode toggle
echo ✅ AI assistant
echo ✅ PWA features
echo ✅ All animations and enhancements
echo.
pause

echo 📝 Adding all files...
git add .

echo 📦 Committing changes...
git commit -m "Add public landing page and deploy all features: OTP, Dark Mode, AI Assistant, PWA"

echo 🚀 Pushing to main branch...
git push origin main

echo.
echo ✅ DEPLOYMENT COMPLETE!
echo.
echo 🌐 Your website will now show:
echo - Public landing page at: https://green-national-zambian-nrc-system.onrender.com
echo - All features visible without login required
echo - OTP system for secure authentication
echo - Dark mode toggle
echo - AI assistant (when logged in)
echo - PWA installation prompts
echo - Mobile responsive design
echo.
echo 🔄 Wait 2-5 minutes for Render to rebuild, then visit your site!
echo.
pause