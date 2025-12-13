@echo off
echo 🔧 FIXING LOGIN REDIRECT ISSUE
echo ===============================
echo.
echo This will fix the button redirect issue:
echo ✅ Landing page buttons now point to login/signup
echo ✅ Apply buttons only show for authenticated users
echo ✅ Added extra authentication checks
echo ✅ Proper URL references (accounts:login, accounts:signup)
echo.
pause

echo 📝 Adding all files...
git add .

echo 📦 Committing changes...
git commit -m "Fix login redirect: Landing page buttons now properly redirect to login/signup"

echo 🚀 Pushing to main branch...
git push origin main

echo.
echo ✅ FIX DEPLOYED!
echo.
echo 🎯 Now when users click "Get Started" on landing page:
echo 1. They will be redirected to signup page
echo 2. After signup, they can login
echo 3. After login, they can access application forms
echo 4. If they try to access forms directly, they'll be redirected to login
echo.
echo 🌐 Test at: https://green-national-zambian-nrc-system.onrender.com
echo.
pause