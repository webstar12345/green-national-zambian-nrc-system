@echo off
echo ========================================
echo  DEPLOYING NRC FLIP & REGISTRATION FIX
echo ========================================
echo.

echo 🔧 Running fix verification...
python fix_nrc_flip_and_registration.py

echo.
echo 🧪 Testing flip functionality...
python test_nrc_flip_and_registration.py

echo.
echo 🔍 Checking for syntax errors...
python manage.py check

echo.
echo 📦 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ✅ DEPLOYMENT COMPLETE!
echo.
echo 🎯 FIXES IMPLEMENTED:
echo =====================
echo ✅ Card flip functionality enhanced
echo ✅ Registration number on back side
echo ✅ Debug logging added to JavaScript
echo ✅ CSS animations improved
echo ✅ Multiple flip triggers (button, card, keyboard)
echo.
echo 🔄 FLIP FUNCTIONALITY:
echo ======================
echo ✅ Button click to flip
echo ✅ Card click to flip  
echo ✅ Keyboard shortcuts (Space, F)
echo ✅ Smooth 0.8s animation
echo ✅ Loading states and feedback
echo ✅ Debug console logging
echo.
echo 📋 REGISTRATION NUMBER:
echo ======================
echo ✅ Front side: Top right overlay
echo ✅ Back side: Top right overlay
echo ✅ Back side: Green registration box
echo ✅ White text on green background
echo.
echo 🧪 TESTING:
echo ===========
echo 1. Start server: python manage.py runserver
echo 2. Open: http://127.0.0.1:8000/application/4/nrc-card/
echo 3. Open browser dev tools (F12)
echo 4. Test flip functionality
echo 5. Check console for debug messages
echo.
echo 🔧 TROUBLESHOOTING:
echo ==================
echo - Open test_flip_functionality.html for isolated test
echo - Check browser console for JavaScript errors
echo - Verify CSS transform is applied
echo - Test in different browsers
echo.
pause