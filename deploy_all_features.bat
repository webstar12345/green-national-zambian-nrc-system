@echo off
echo 🚀 DEPLOYING ALL FEATURES TO RENDER
echo ===================================
echo.
echo This will push all your features to the deployed website:
echo - OTP System
echo - Dark Mode
echo - AI Assistant  
echo - PWA Features
echo - Animations
echo - Google OAuth
echo - Landing Page
echo.
pause

echo 📝 Adding all files...
git add .

echo 📦 Committing changes...
git commit -m "Deploy all features: OTP, Dark Mode, AI Assistant, PWA, Animations, OAuth"

echo 🚀 Pushing to main branch...
git push origin main

echo.
echo ✅ DEPLOYMENT COMPLETE!
echo.
echo 🔄 Render will now rebuild with all your features:
echo - Check your Render dashboard for deployment progress
echo - Wait for build to complete (usually 2-5 minutes)
echo - Your features should then be visible on the live site
echo.
echo 🌐 Features that will be available:
echo ✅ OTP verification system
echo ✅ Dark mode toggle
echo ✅ AI chat assistant
echo ✅ PWA installation
echo ✅ Smooth animations
echo ✅ Google OAuth login
echo ✅ Mobile responsive design
echo.
pause