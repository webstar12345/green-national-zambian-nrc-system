#!/usr/bin/env python
"""
Test OTP email functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from accounts.otp_service import OTPService
from django.contrib.auth import get_user_model

User = get_user_model()

def test_otp_email():
    """Test OTP email sending"""
    print("🧪 Testing OTP Email Functionality")
    print("=" * 40)
    
    # Test email configuration
    from django.conf import settings
    print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
    print(f"📧 Email Host: {getattr(settings, 'EMAIL_HOST', 'Not configured')}")
    print(f"📧 Email Port: {getattr(settings, 'EMAIL_PORT', 'Not configured')}")
    print(f"📧 Email User: {getattr(settings, 'EMAIL_HOST_USER', 'Not configured')}")
    print(f"📧 Email TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not configured')}")
    print(f"📧 Default From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"📧 DEBUG Mode: {settings.DEBUG}")
    
    # Check if we're in production mode
    if not settings.DEBUG:
        print("\n🚨 PRODUCTION MODE DETECTED")
        email_password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        if not email_password or email_password == 'REPLACE_WITH_GMAIL_APP_PASSWORD':
            print("❌ EMAIL_HOST_PASSWORD not configured!")
            print("🔧 Please update EMAIL_HOST_PASSWORD on Render with Gmail app password")
            print("📖 See FIX_OTP_EMAIL_ISSUE.md for instructions")
            return
        else:
            print("✅ EMAIL_HOST_PASSWORD is configured")
    
    # Generate test OTP
    test_otp = OTPService.generate_otp_code()
    print(f"\n🔢 Generated Test OTP: {test_otp}")
    
    # Get test email from user input
    import sys
    if len(sys.argv) > 1:
        test_email = sys.argv[1]
    else:
        test_email = input("\n📧 Enter your email to test OTP delivery: ").strip()
        if not test_email:
            test_email = "test@example.com"
    
    test_name = "Test User"
    
    print(f"\n📤 Attempting to send OTP email to: {test_email}")
    
    try:
        success = OTPService.send_otp_email(test_email, test_otp, test_name)
        
        if success:
            print("✅ OTP email sent successfully!")
            print("\n📋 Email should contain:")
            print(f"   - Subject: NRC Zambia - Verification Code")
            print(f"   - OTP Code: {test_otp}")
            print(f"   - Recipient: {test_email}")
            print(f"   - HTML formatted content")
            
            if not settings.DEBUG:
                print(f"\n📬 Check your email inbox: {test_email}")
                print("📁 Also check spam/junk folder")
        else:
            print("❌ Failed to send OTP email")
            print("\n🔍 Possible issues:")
            print("   - Email configuration not set up")
            print("   - SMTP credentials missing or incorrect")
            print("   - Network connectivity issues")
            print("   - Gmail app password not configured")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        print("\n🔍 This usually means:")
        print("   - SMTP authentication failed")
        print("   - Gmail app password is incorrect")
        print("   - Network/firewall issues")
    
    # Test OTP validation
    print(f"\n🔍 Testing OTP validation:")
    print(f"   - Valid format check: {OTPService.validate_otp_format(test_otp)}")
    print(f"   - Invalid format check: {OTPService.validate_otp_format('12345')}")
    print(f"   - Invalid format check: {OTPService.validate_otp_format('abcdef')}")
    
    # Production-specific advice
    if not settings.DEBUG:
        print(f"\n🚀 Production Environment Tips:")
        print("   - Ensure Gmail 2FA is enabled")
        print("   - Use Gmail App Password (not regular password)")
        print("   - Check Render environment variables")
        print("   - Monitor Render logs for SMTP errors")

if __name__ == '__main__':
    test_otp_email()