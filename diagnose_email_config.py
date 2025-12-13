#!/usr/bin/env python
"""
Diagnose Email Configuration Issues
Run this script to check if email is properly configured
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from accounts.otp_service import OTPService

def diagnose_email_config():
    """Diagnose email configuration issues"""
    print("🔍 Email Configuration Diagnosis")
    print("=" * 50)
    
    # Check Django settings
    print("\n📧 Django Email Settings:")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    if hasattr(settings, 'EMAIL_HOST'):
        print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        
        # Check password (without revealing it)
        password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        if password:
            if password == 'REPLACE_WITH_GMAIL_APP_PASSWORD':
                print("   EMAIL_HOST_PASSWORD: ❌ PLACEHOLDER - NEEDS REAL APP PASSWORD")
            elif len(password) == 16 and ' ' not in password:
                print("   EMAIL_HOST_PASSWORD: ✅ Configured (16 chars, looks like app password)")
            elif len(password) < 16:
                print("   EMAIL_HOST_PASSWORD: ⚠️  Configured but seems short for app password")
            else:
                print("   EMAIL_HOST_PASSWORD: ✅ Configured")
        else:
            print("   EMAIL_HOST_PASSWORD: ❌ NOT SET")
    else:
        print("   SMTP Settings: ❌ NOT CONFIGURED (using console backend)")
    
    # Check environment variables
    print("\n🌍 Environment Variables:")
    env_vars = ['EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL']
    for var in env_vars:
        value = os.environ.get(var, 'NOT SET')
        if var == 'EMAIL_HOST_PASSWORD':
            if value == 'NOT SET':
                print(f"   {var}: ❌ {value}")
            elif value == 'REPLACE_WITH_GMAIL_APP_PASSWORD':
                print(f"   {var}: ❌ PLACEHOLDER VALUE")
            else:
                print(f"   {var}: ✅ SET (length: {len(value)})")
        else:
            print(f"   {var}: {'✅' if value != 'NOT SET' else '❌'} {value}")
    
    # Test basic email sending
    print("\n🧪 Testing Email Functionality:")
    
    if settings.DEBUG:
        print("   Mode: Development (console backend)")
        print("   ✅ Emails will be printed to console")
    else:
        print("   Mode: Production (SMTP backend)")
        
        # Check if we can send a test email
        test_email = "test@example.com"
        try:
            print(f"   📤 Testing simple email to {test_email}...")
            send_mail(
                'Test Email from NRC System',
                'This is a test email to verify SMTP configuration.',
                settings.DEFAULT_FROM_EMAIL,
                [test_email],
                fail_silently=False,
            )
            print("   ✅ Basic email sending works!")
        except Exception as e:
            print(f"   ❌ Basic email failed: {e}")
            
            # Provide specific guidance
            error_str = str(e).lower()
            if "authentication failed" in error_str:
                print("   🔧 Fix: Update EMAIL_HOST_PASSWORD with Gmail app password")
            elif "connection refused" in error_str:
                print("   🔧 Fix: Check EMAIL_HOST and EMAIL_PORT settings")
            elif "timeout" in error_str:
                print("   🔧 Fix: Check network connectivity and firewall")
    
    # Test OTP service
    print("\n🔢 Testing OTP Service:")
    try:
        otp_code = OTPService.generate_otp_code()
        print(f"   ✅ OTP Generation: {otp_code}")
        
        # Test OTP email (won't actually send in production without real email)
        if settings.DEBUG:
            success = OTPService.send_otp_email("test@example.com", otp_code, "Test User")
            print(f"   ✅ OTP Email Service: {'Working' if success else 'Failed'}")
        else:
            print("   ⚠️  OTP Email: Skipped in production (would need real email)")
            
    except Exception as e:
        print(f"   ❌ OTP Service Error: {e}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    
    if settings.DEBUG:
        print("   📝 You're in development mode - emails go to console")
        print("   🚀 For production: Set DEBUG=False and configure SMTP")
    else:
        password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        if not password or password == 'REPLACE_WITH_GMAIL_APP_PASSWORD':
            print("   🔑 URGENT: Set up Gmail App Password")
            print("   📖 See FIX_OTP_EMAIL_ISSUE.md for instructions")
        else:
            print("   ✅ Email configuration looks good")
            print("   🧪 Test with real email address to confirm")

if __name__ == '__main__':
    diagnose_email_config()