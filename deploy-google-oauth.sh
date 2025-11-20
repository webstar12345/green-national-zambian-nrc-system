#!/bin/bash
# Deploy Google OAuth to Render

echo "========================================"
echo "Deploying Google OAuth Login"
echo "========================================"
echo ""

git add requirements.txt
git add nrc_system/settings.py
git add nrc_system/urls.py
git add templates/accounts/login.html
git add templates/accounts/signup.html
git add accounts/management/commands/setup_google_oauth.py
git add GOOGLE_OAUTH_SETUP.md
git add QUICK_GOOGLE_OAUTH.md
git add .env.example
git add push-google-oauth.bat
git add deploy-google-oauth.sh

git commit -m "Add Google OAuth login functionality"
git push origin main

echo ""
echo "========================================"
echo "Google OAuth Code Deployed!"
echo "========================================"
echo ""
echo "NEXT STEPS:"
echo "1. Follow QUICK_GOOGLE_OAUTH.md to set up Google Cloud Console"
echo "2. Add credentials to Render environment variables"
echo "3. After deployment, configure in Django admin"
echo "4. Test at: https://nrccard.onrender.com/accounts/login/"
echo ""
