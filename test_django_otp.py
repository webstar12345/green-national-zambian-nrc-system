#!/usr/bin/env python3
"""
Test OTP functionality within Django environment
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

def test_django_otp():
    print("🧪 TESTING DJANGO OTP FUNCTIONALITY")
    print("=" * 40)
    
    from accounts.otp_service import OTPService
    from django.conf import settings
    
    # Check Django email settings
    print("🔧 Django Email Settings:")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"   EMAIL_HOST_PASSWORD: {'***' if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    
    # Test OTP generation
    print(f"\n🔢 Testing OTP Generation...")
    otp_code = OTPService.generate_otp_code()
    print(f"   Generated OTP: {otp_code}")
    
    # Test OTP email sending through Django
    print(f"\n📤 Testing OTP Email via Django...")
    test_email = "simoongalaurent427@gmail.com"
    test_name = "Django Test User"
    
    try:
        success = OTPService.send_otp_email(test_email, otp_code, test_name)
        
        if success:
            print("✅ SUCCESS! Django OTP email sent!")
            print(f"📧 Check email: {test_email}")
            print(f"🔢 OTP code: {otp_code}")
            print(f"\n🎯 Your Django OTP system is working!")
            return True
        else:
            print("❌ Django OTP email failed")
            return False
            
    except Exception as e:
        print(f"❌ Django OTP error: {e}")
        return False

if __name__ == "__main__":
    success = test_django_otp()
    
    if success:
        print(f"\n🎉 DJANGO OTP IS WORKING!")
        print(f"   Start server: python manage.py runserver")
        print(f"   Test login: http://localhost:8000/accounts/login/")
    else:
        print(f"\n🔧 Django OTP needs debugging")
        print(f"   Check Django settings configuration")