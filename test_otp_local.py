#!/usr/bin/env python
"""
Test OTP Email Locally
Run this after updating .env with real Gmail app password
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from accounts.otp_service import OTPService

def test_otp_local():
    """Test OTP email with real Gmail credentials"""
    print("🧪 Testing OTP Email Locally")
    print("=" * 40)
    
    # Generate test OTP
    otp_code = OTPService.generate_otp_code()
    print(f"Generated OTP: {otp_code}")
    
    # Test email (replace with your email)
    test_email = "simoongalaurent427@gmail.com"  # Use your own email for testing
    
    print(f"\n📧 Sending OTP to: {test_email}")
    print("⏳ Please wait...")
    
    try:
        success = OTPService.send_otp_email(test_email, otp_code, "Test User")
        
        if success:
            print("✅ SUCCESS! OTP email sent successfully")
            print(f"📱 Check your email for OTP: {otp_code}")
            print("🎉 Your Gmail SMTP configuration is working!")
        else:
            print("❌ FAILED! OTP email could not be sent")
            print("🔧 Check your Gmail app password in .env file")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("🔧 Make sure you've updated .env with real Gmail app password")

if __name__ == '__main__':
    test_otp_local()