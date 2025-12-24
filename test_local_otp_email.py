#!/usr/bin/env python3
"""
Test OTP email functionality on localhost
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

def test_local_otp_email():
    print("📧 TESTING LOCAL OTP EMAIL FUNCTIONALITY")
    print("=" * 50)
    
    from django.conf import settings
    from accounts.otp_service import OTPService
    
    # Check if we're in DEBUG mode (local)
    if not settings.DEBUG:
        print("⚠️  WARNING: Not in DEBUG mode. This test is for local development.")
        return
    
    # Display current email settings
    print("🔧 Current Email Configuration:")
    print(f"   EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
    print(f"   EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Not set')}")
    print(f"   EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
    print(f"   EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
    print(f"   EMAIL_HOST_PASSWORD: {'***' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else 'Not set'}")
    
    # Test OTP generation
    print(f"\n🔢 Testing OTP Generation...")
    test_otp = OTPService.generate_otp_code()
    print(f"   Generated OTP: {test_otp}")
    
    # Test email sending
    print(f"\n📤 Testing OTP Email Sending...")
    test_email = "simoongalaurent427@gmail.com"
    test_name = "Test User"
    
    try:
        success = OTPService.send_otp_email(test_email, test_otp, test_name)
        
        if success:
            print("✅ SUCCESS! OTP email sent successfully!")
            print(f"📧 Check your email: {test_email}")
            print(f"🔢 Look for OTP code: {test_otp}")
            print(f"\n🎯 Your localhost OTP system is working perfectly!")
            
            # Test login flow
            print(f"\n🧪 To test full login flow:")
            print(f"1. Start your Django server: python manage.py runserver")
            print(f"2. Go to: http://localhost:8000/accounts/login/")
            print(f"3. Try to login with your credentials")
            print(f"4. Check email for OTP code")
            print(f"5. Enter OTP to complete login")
            
            return True
        else:
            print("❌ FAILED: Email sending returned False")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
        # Provide specific troubleshooting
        error_str = str(e).lower()
        if "authentication failed" in error_str:
            print(f"\n🔐 GMAIL AUTHENTICATION ISSUE:")
            print(f"   - Check if app password is correct: sghuygvzhowzrdmm")
            print(f"   - Verify 2FA is enabled on Gmail account")
            print(f"   - Try generating a new app password")
        elif "network" in error_str or "unreachable" in error_str:
            print(f"\n🌐 NETWORK ISSUE:")
            print(f"   - Check internet connection")
            print(f"   - Verify firewall isn't blocking SMTP")
            print(f"   - Try different network if on corporate/school WiFi")
        elif "timeout" in error_str:
            print(f"\n⏰ TIMEOUT ISSUE:")
            print(f"   - Gmail servers may be slow")
            print(f"   - Try again in a few minutes")
        else:
            print(f"\n🔍 UNKNOWN ERROR:")
            print(f"   - Error details: {e}")
            print(f"   - Check .env file configuration")
        
        return False

def check_env_file():
    """Check .env file configuration"""
    print(f"\n📄 Checking .env file...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found!")
        return False
    
    content = env_file.read_text()
    
    required_vars = [
        'EMAIL_HOST=smtp.gmail.com',
        'EMAIL_PORT=587',
        'EMAIL_USE_TLS=True',
        'EMAIL_HOST_USER=simoongalaurent427@gmail.com',
        'EMAIL_HOST_PASSWORD=sghuygvzhowzrdmm'
    ]
    
    print("✅ .env file found. Checking configuration:")
    
    for var in required_vars:
        if var in content:
            print(f"   ✅ {var}")
        else:
            print(f"   ❌ Missing: {var}")
    
    return True

if __name__ == "__main__":
    print("🏠 LOCAL OTP EMAIL TEST")
    print("=" * 30)
    
    # Check environment
    check_env_file()
    
    # Test email functionality
    success = test_local_otp_email()
    
    if success:
        print(f"\n🎉 LOCAL OTP EMAIL IS WORKING!")
        print(f"   - Gmail SMTP connection successful")
        print(f"   - OTP emails will be delivered")
        print(f"   - Ready for local development and testing")
    else:
        print(f"\n🚨 LOCAL OTP EMAIL NEEDS FIXING")
        print(f"   - Check Gmail app password")
        print(f"   - Verify internet connection")
        print(f"   - Review error messages above")