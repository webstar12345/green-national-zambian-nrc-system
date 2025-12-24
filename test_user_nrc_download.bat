@echo off
echo ========================================
echo 🧪 TESTING USER NRC DOWNLOAD ACCESS
echo ========================================
echo.

echo 📋 Checking NRC download status...
python check_nrc_download_status.py

echo.
echo 🧪 Testing user access...
python test_user_nrc_access.py

echo.
echo ========================================
echo 💡 USER INSTRUCTIONS:
echo ========================================
echo.
echo 1. Login as: mysister@123 (password: mysister@123)
echo 2. Go to Home page - look for notification alerts
echo 3. Click "Download Now" button in notifications
echo 4. OR go to "My Applications" and click download buttons
echo 5. OR visit Application Detail page for full options
echo.
echo 📱 Available download formats:
echo    - PNG (Front Side)
echo    - PNG (Back Side) 
echo    - ZIP (Both Sides)
echo.
echo 🎯 Direct URLs for Application #1:
echo    - View Details: /application/1/
echo    - View NRC Card: /application/1/nrc-card/
echo    - Download Front: /application/1/download/front/
echo    - Download Back: /application/1/download/back/
echo    - Download Both: /application/1/download/both/
echo.
echo ✅ If you see green "NRC Ready!" messages, downloads are available!
echo.
pause