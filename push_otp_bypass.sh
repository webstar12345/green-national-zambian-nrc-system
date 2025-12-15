#!/bin/bash
# Temporary OTP bypass for testing - Run this in Git Bash

echo "🔧 TEMPORARY: Pushing OTP bypass for testing"
echo "============================================"

git add .
git commit -m "TEMPORARY: Bypass OTP for testing while fixing email configuration

🔧 TEMPORARY FIX:
- Skip OTP verification if email sending fails
- Allow direct login for testing purposes
- User gets logged in automatically if email fails
- Can be reverted once email is working

🎯 PURPOSE:
- Test the rest of the system functionality
- Verify login/dashboard works without OTP
- Isolate email configuration issues
- Allow system testing while fixing SMTP

⚠️ NOTE: This is temporary - will revert once email works"

echo ""
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ TEMPORARY OTP BYPASS PUSHED!"
echo ""
echo "🎯 WHAT THIS DOES:"
echo "- Login will work even if email fails"
echo "- User gets logged in directly"
echo "- No more 'Failed to send OTP' blocking login"
echo "- You can test the dashboard and other features"
echo ""
echo "🔧 MEANWHILE, SET THESE IN RENDER.COM:"
echo "EMAIL_HOST_PASSWORD=uroaoegylbpusjfy"
echo "EMAIL_HOST_USER=simoongalaurent427@gmail.com"
echo ""
echo "🌐 Test login at: https://green-national-zambian-nrc-system.onrender.com"