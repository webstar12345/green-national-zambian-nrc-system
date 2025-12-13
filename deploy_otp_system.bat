@echo off
echo 🔐 DEPLOYING OTP EMAIL VERIFICATION SYSTEM
echo ==========================================
echo.
echo This will deploy the complete OTP system:
echo ✅ OTP verification for login
echo ✅ OTP verification for registration  
echo ✅ HTML email templates
echo ✅ Enhanced security flow
echo ✅ Resend OTP functionality
echo.
pause

echo 📝 Adding all files...
git add .

echo 📦 Committing changes...
git commit -m "Deploy OTP email verification system: Login and registration with email OTP codes"

echo 🚀 Pushing to main branch...
git push origin main

echo.
echo ✅ OTP SYSTEM DEPLOYED!
echo.
echo 🔐 How the OTP system works:
echo.
echo 📝 REGISTRATION FLOW:
echo 1. User fills signup form
echo 2. Account created but not logged in
echo 3. OTP sent to user's email
echo 4. User enters OTP code
echo 5. Account verified and user logged in
echo.
echo 🔑 LOGIN FLOW:
echo 1. User enters username/password
echo 2. Credentials verified
echo 3. OTP sent to user's email
echo 4. User enters OTP code
echo 5. User logged in successfully
echo.
echo 📧 EMAIL FEATURES:
echo - HTML formatted emails
echo - Professional NRC Zambia branding
echo - Security warnings and tips
echo - 10-minute expiration notice
echo.
echo 🌐 Test at: https://green-national-zambian-nrc-system.onrender.com
echo.
pause