#!/usr/bin/env python3
"""
Fix Django email configuration
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

def fix_django_email():
    print("🔧 FIXING DJANGO EMAIL CONFIGURATION")
    print("=" * 40)
    
    from django.conf import settings
    
    # Check current settings
    print("📧 Current Django Email Settings:")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"   EMAIL_HOST_PASSWORD: {'***' if settings.EMAIL_HOST_PASSWORD else 'EMPTY!'}")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    
    # Check if password is loaded
    if not settings.EMAIL_HOST_PASSWORD:
        print(f"\n❌ EMAIL_HOST_PASSWORD is empty!")
        print(f"🔧 Manually setting email configuration...")
        
        # Manually set email settings
        settings.EMAIL_HOST = 'smtp.gmail.com'
        settings.EMAIL_PORT = 587
        settings.EMAIL_USE_TLS = True
        settings.EMAIL_HOST_USER = 'simoongalaurent427@gmail.com'
        settings.EMAIL_HOST_PASSWORD = 'sghuygvzhowzrdmm'
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        
        print(f"✅ Email settings updated manually")
    
    # Test email sending
    print(f"\n🧪 Testing Django email sending...")
    
    try:
        from django.core.mail import send_mail
        
        result = send_mail(
            subject='Django OTP Test - Fixed Configuration',
            message=f'''
Hello!

This is a test from Django with fixed email configuration.

Settings used:
- EMAIL_HOST: {settings.EMAIL_HOST}
- EMAIL_PORT: {settings.EMAIL_PORT}
- EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}
- EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}

If you receive this, Django OTP emails will work!

Time: {django.utils.timezone.now()}
            ''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['simoongalaurent427@gmail.com'],
            fail_silently=False,
        )
        
        if result == 1:
            print("✅ SUCCESS! Django email is now working!")
            print(f"📧 Check your email for confirmation")
            return True
        else:
            print("❌ Email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ Django email error: {e}")
        
        if "authentication failed" in str(e).lower():
            print(f"\n🔐 Gmail authentication issue in Django")
            print(f"   - Check .env file is in correct location")
            print(f"   - Verify python-decouple is loading variables")
        
        return False

def create_env_loader():
    """Create a manual .env loader for Django"""
    print(f"\n🔧 Creating manual .env loader...")
    
    env_file = Path('.env')
    if env_file.exists():
        content = env_file.read_text()
        
        # Extract email settings
        email_vars = {}
        for line in content.split('\n'):
            if line.startswith('EMAIL_'):
                key, value = line.split('=', 1)
                email_vars[key] = value
        
        print(f"📄 Found email variables in .env:")
        for key, value in email_vars.items():
            masked_value = '***' if 'PASSWORD' in key else value
            print(f"   {key}={masked_value}")
        
        return email_vars
    else:
        print(f"❌ .env file not found!")
        return {}

if __name__ == "__main__":
    # Check .env file
    env_vars = create_env_loader()
    
    # Fix Django email
    success = fix_django_email()
    
    if success:
        print(f"\n🎉 DJANGO EMAIL IS FIXED!")
        print(f"   - OTP emails will now work in Django")
        print(f"   - Test login at: http://localhost:8000/accounts/login/")
    else:
        print(f"\n🔧 Manual fix needed:")
        print(f"   - Check .env file location")
        print(f"   - Verify python-decouple installation")
        print(f"   - Consider manual settings override")