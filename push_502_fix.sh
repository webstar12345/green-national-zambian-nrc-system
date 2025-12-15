#!/bin/bash
# Emergency 502 fix - Run this in Git Bash

echo "🚨 EMERGENCY: Pushing 502 error fix to GitHub"
echo "============================================="

git add .
git commit -m "EMERGENCY: Fix 502 error during login - Memory optimization + timeout protection

🚨 CRITICAL 502 FIX:
- Added timeout protection for OTP email sending
- Memory optimization in login flow
- Better error handling to prevent worker crashes
- Session storage before email sending (crash protection)

🛡️ WORKER PROTECTION:
- 30-second timeout for email operations
- Graceful fallback if email sending fails
- User can still access OTP page and resend
- Prevents 502 Bad Gateway errors

⚡ MEMORY OPTIMIZATION:
- Reduced memory usage during email sending
- Better exception handling
- Session management improvements"

echo ""
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ 502 FIX PUSHED TO GITHUB!"
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Go to Render.com Dashboard → Environment"
echo "2. Add: WEB_CONCURRENCY=1"
echo "3. Add: GUNICORN_CMD_ARGS=--timeout 300 --max-requests 100"
echo "4. Add: EMAIL_HOST_PASSWORD=uroaoegylbpusjfy"
echo "5. Wait for deployment"
echo "6. Test login (should work without 502)"
echo ""
echo "🌐 Your site: https://green-national-zambian-nrc-system.onrender.com"