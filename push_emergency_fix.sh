#!/bin/bash
# Emergency production fix - Run this in Git Bash

echo "🚨 EMERGENCY: Pushing production fix to GitHub"
echo "=============================================="

git add .
git commit -m "EMERGENCY: Production restore - Fixed shell scripts + OTP security

🚨 CRITICAL PRODUCTION FIX:
- Fixed Unix line endings in build.sh and start.sh  
- Memory optimization: gunicorn.conf.py with single worker
- Security: Updated Gmail app password (uroaoegylbpusjfy)
- Performance: Reduced memory usage, increased timeouts

🛡️ SECURITY BREACH RESOLVED:
- New Gmail app password deployed
- Removed exposed credentials  
- Local testing: ✅ WORKING

⚡ MEMORY OPTIMIZATION:
- Single worker to prevent SIGKILL
- 120s timeout to prevent worker kills
- Memory cleanup and optimization"

echo ""
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ EMERGENCY FIX PUSHED TO GITHUB!"
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Go to Render.com Dashboard"
echo "2. Update Build/Start commands:"
echo "   Build: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
echo "   Start: gunicorn nrc_system.wsgi:application"
echo "3. Set EMAIL_HOST_PASSWORD=uroaoegylbpusjfy"
echo "4. Wait for deployment"
echo "5. Test OTP emails"
echo ""
echo "🌐 Your site: https://green-national-zambian-nrc-system.onrender.com"