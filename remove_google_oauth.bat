@echo off
echo ========================================
echo REMOVING GOOGLE OAUTH FROM LOGIN PAGES
echo ========================================
echo.

echo 🔧 Changes Applied:
echo - Removed Google OAuth login button from login page
echo - Removed Google OAuth signup button from signup page
echo - Cleaned up dividers and social login sections
echo - Simplified authentication to email/password only
echo.

echo 📋 Files Modified:
echo - templates/accounts/login.html (removed Google login)
echo - templates/accounts/signup.html (removed Google signup)
echo.

echo 🚀 Pushing changes to Git...
git add templates/accounts/login.html
git add templates/accounts/signup.html
git add remove_google_oauth.bat

git commit -m "🔒 REMOVE GOOGLE OAUTH: Simplified authentication to email/password only

🎯 Changes:
- Removed Google OAuth login from login page
- Removed Google OAuth signup from signup page
- Cleaned up social login dividers and sections
- Streamlined user experience to single authentication method

✅ Benefits:
- Simplified user interface
- Reduced complexity
- Faster login process
- No external dependencies for authentication
- Better control over user registration flow"

echo.
echo ✅ Google OAuth removed from login and signup pages!
echo.
echo 📋 Current Authentication Methods:
echo - Username/Email + Password + OTP verification
echo - Admin bypass (no OTP for admin users)
echo - Password reset via email
echo.
echo 🔧 To test:
echo 1. Visit login page - no Google button
echo 2. Visit signup page - no Google button  
echo 3. Test regular login/signup flow
echo.
pause