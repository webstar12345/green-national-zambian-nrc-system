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
    print(f"📧 Default From Email: {settings.DEFAULT_FROM_EMAIL}")
    
    # Generate test OTP
    test_otp = OTPService.generate_otp_code()
    print(f"\n🔢 Generated Test OTP: {test_otp}")
    
    # Test email sending (you can replace with your email for testing)
    test_email = "test@example.com"  # Replace with your email for testing
    test_name = "Test User"
    
    print(f"\n📤 Attempting to send OTP email to: {test_email}")
    
    success = OTPService.send_otp_email(test_email, test_otp, test_name)
    
    if success:
        print("✅ OTP email sent successfully!")
        print("\n📋 Email should contain:")
        print(f"   - Subject: NRC Zambia - Verification Code")
        print(f"   - OTP Code: {test_otp}")
        print(f"   - Recipient: {test_email}")
        print(f"   - HTML formatted content")
    else:
        print("❌ Failed to send OTP email")
        print("\n🔍 Possible issues:")
        print("   - Email configuration not set up")
        print("   - SMTP credentials missing")
        print("   - Network connectivity issues")
        print("   - Template rendering errors")
    
    # Test OTP validation
    print(f"\n🔍 Testing OTP validation:")
    print(f"   - Valid format check: {OTPService.validate_otp_format(test_otp)}")
    print(f"   - Invalid format check: {OTPService.validate_otp_format('12345')}")
    print(f"   - Invalid format check: {OTPService.validate_otp_format('abcdef')}")

if __name__ == '__main__':
    test_otp_email()