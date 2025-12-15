#!/usr/bin/env python3
"""
Diagnose production login issues
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

def diagnose_login_issues():
    print("🔍 DIAGNOSING PRODUCTION LOGIN ISSUES")
    print("=" * 50)
    
    # Check database connectivity
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection: WORKING")
    except Exception as e:
        print(f"❌ Database connection: FAILED - {e}")
        return
    
    # Check user model
    try:
        from accounts.models import User
        user_count = User.objects.count()
        print(f"✅ User model: WORKING ({user_count} users)")
    except Exception as e:
        print(f"❌ User model: FAILED - {e}")
        return
    
    # Check OTP model
    try:
        from accounts.models import OTP
        otp_count = OTP.objects.count()
        print(f"✅ OTP model: WORKING ({otp_count} OTPs)")
    except Exception as e:
        print(f"❌ OTP model: FAILED - {e}")
    
    # Check email configuration
    try:
        from django.conf import settings
        email_config = {
            'EMAIL_HOST': getattr(settings, 'EMAIL_HOST', 'Not set'),
            'EMAIL_PORT': getattr(settings, 'EMAIL_PORT', 'Not set'),
            'EMAIL_USE_TLS': getattr(settings, 'EMAIL_USE_TLS', 'Not set'),
            'EMAIL_HOST_USER': getattr(settings, 'EMAIL_HOST_USER', 'Not set'),
            'EMAIL_HOST_PASSWORD': '***' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else 'Not set',
        }
        print("✅ Email configuration:")
        for key, value in email_config.items():
            print(f"   {key}: {value}")
    except Exception as e:
        print(f"❌ Email configuration: FAILED - {e}")
    
    # Test OTP service
    try:
        from accounts.otp_service import OTPService
        otp_service = OTPService()
        print("✅ OTP service: IMPORTED")
        
        # Test email sending (dry run)
        print("🧪 Testing email configuration...")
        from django.core.mail import get_connection
        connection = get_connection()
        print(f"✅ Email backend: {connection.__class__.__name__}")
        
    except Exception as e:
        print(f"❌ OTP service: FAILED - {e}")
    
    # Check memory usage
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"💾 Memory usage: {memory.percent}% ({memory.used // 1024 // 1024}MB used)")
    except ImportError:
        print("💾 Memory info: psutil not available")
    except Exception as e:
        print(f"💾 Memory info: {e}")
    
    print("\n🎯 LIKELY ISSUES:")
    print("1. Memory constraints causing worker timeouts")
    print("2. OTP email sending process crashes the worker")
    print("3. Database queries timing out")
    print("4. Missing environment variables in production")
    
    print("\n🛠️ RECOMMENDED FIXES:")
    print("1. Add memory optimization to Render.com:")
    print("   WEB_CONCURRENCY=1")
    print("   GUNICORN_CMD_ARGS=--timeout 120 --max-requests 1000")
    print("2. Check Render.com logs for specific errors")
    print("3. Verify EMAIL_HOST_PASSWORD is set in production")
    print("4. Consider upgrading Render.com plan for more memory")

if __name__ == "__main__":
    diagnose_login_issues()