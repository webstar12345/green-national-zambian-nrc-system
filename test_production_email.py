#!/usr/bin/env python3
"""
Test email sending in production environment
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

def test_production_email():
    print("🧪 TESTING PRODUCTION EMAIL CONFIGURATION")
    print("=" * 50)
    
    from django.conf import settings
    from django.core.mail import send_mail, get_connection
    from django.core.mail.backends.smtp import EmailBackend
    
    # Check email settings
    print("📧 Email Configuration:")
    print(f"   EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
    print(f"   EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Not set')}")
    print(f"   EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
    print(f"   EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
    print(f"   EMAIL_HOST_PASSWORD: {'***' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else 'Not set'}")
    print(f"   DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")
    
    # Test connection
    print("\n🔌 Testing SMTP Connection...")
    try:
        connection = get_connection()
        connection.open()
        print("✅ SMTP connection successful!")
        connection.close()
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        return False
    
    # Test email sending
    print("\n📤 Testing Email Sending...")
    try:
        result = send_mail(
            subject='NRC System - Production Email Test',
            message='This is a test email from your NRC system production environment. If you receive this, email configuration is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['simoongalaurent427@gmail.com'],
            fail_silently=False,
        )
        
        if result == 1:
            print("✅ Test email sent successfully!")
            print("📬 Check your inbox (and spam folder) for the test email")
            return True
        else:
            print("❌ Email sending failed - no error but result was 0")
            return False
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Email sending failed: {error_msg}")
        
        # Provide specific diagnostics
        if "authentication failed" in error_msg.lower():
            print("\n🔐 DIAGNOSIS: Gmail Authentication Failed")
            print("   - App password may be expired or incorrect")
            print("   - Check Gmail security settings")
            print("   - Generate new app password if needed")
        elif "connection" in error_msg.lower():
            print("\n🌐 DIAGNOSIS: Network Connection Issue")
            print("   - SMTP port 587 may be blocked")
            print("   - Check Render.com network policies")
            print("   - Try alternative email service")
        elif "timeout" in error_msg.lower():
            print("\n⏰ DIAGNOSIS: Connection Timeout")
            print("   - Gmail SMTP server may be slow")
            print("   - Network latency issues")
            print("   - Try increasing timeout settings")
        else:
            print(f"\n🔍 DIAGNOSIS: Unknown Error")
            print(f"   - Error details: {error_msg}")
        
        return False

if __name__ == "__main__":
    success = test_production_email()
    
    if success:
        print("\n🎉 EMAIL CONFIGURATION IS WORKING!")
        print("   - OTP emails should work now")
        print("   - Try logging in again")
    else:
        print("\n🚨 EMAIL CONFIGURATION NEEDS FIXING")
        print("   - Check the diagnosis above")
        print("   - May need new Gmail app password")
        print("   - Consider alternative email service")