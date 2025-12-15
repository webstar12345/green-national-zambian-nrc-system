#!/usr/bin/env python
"""
Advanced OTP Email Troubleshooting for Production
This script will help identify exactly why OTP emails aren't working
"""
import os
import sys
import django
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from accounts.otp_service import OTPService
import logging

def test_smtp_connection():
    """Test direct SMTP connection without Django"""
    print("🔌 Testing Direct SMTP Connection...")
    print("=" * 50)
    
    # Get credentials from environment or settings
    host = getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com')
    port = getattr(settings, 'EMAIL_PORT', 587)
    username = getattr(settings, 'EMAIL_HOST_USER', '')
    password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    use_tls = getattr(settings, 'EMAIL_USE_TLS', True)
    
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
    print(f"Use TLS: {use_tls}")
    print()
    
    if not username or not password:
        print("❌ SMTP credentials not configured!")
        return False
    
    try:
        print("📡 Connecting to SMTP server...")
        server = smtplib.SMTP(host, port)
        
        print("🔒 Starting TLS...")
        if use_tls:
            server.starttls()
        
        print("🔐 Authenticating...")
        server.login(username, password)
        
        print("✅ SMTP Connection Successful!")
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Failed: {e}")
        print("🔧 Fix: Check Gmail app password")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"❌ SMTP Connection Failed: {e}")
        print("🔧 Fix: Check host/port settings")
        return False
    except Exception as e:
        print(f"❌ SMTP Error: {e}")
        return False

def test_django_email():
    """Test Django email sending"""
    print("\n📧 Testing Django Email System...")
    print("=" * 50)
    
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Debug Mode: {settings.DEBUG}")
    
    if settings.DEBUG:
        print("⚠️  You're in DEBUG mode - emails go to console!")
        print("🔧 Set DEBUG=False in production")
        return True
    
    test_email = "simoongalaurent427@gmail.com"  # Your email for testing
    
    try:
        print(f"📤 Sending test email to {test_email}...")
        
        send_mail(
            'Test Email from NRC System',
            'This is a test email to verify Django email configuration.',
            settings.DEFAULT_FROM_EMAIL,
            [test_email],
            fail_silently=False,
        )
        
        print("✅ Django email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Django email failed: {e}")
        return False

def test_otp_service():
    """Test OTP service specifically"""
    print("\n🔢 Testing OTP Service...")
    print("=" * 50)
    
    try:
        # Generate OTP
        otp_code = OTPService.generate_otp_code()
        print(f"✅ OTP Generated: {otp_code}")
        
        # Test email sending
        test_email = "simoongalaurent427@gmail.com"
        print(f"📧 Sending OTP email to {test_email}...")
        
        success = OTPService.send_otp_email(test_email, otp_code, "Test User")
        
        if success:
            print("✅ OTP Email Service Working!")
            print(f"📱 Check {test_email} for OTP: {otp_code}")
        else:
            print("❌ OTP Email Service Failed!")
            
        return success
        
    except Exception as e:
        print(f"❌ OTP Service Error: {e}")
        return False

def check_environment():
    """Check environment configuration"""
    print("\n🌍 Environment Configuration Check...")
    print("=" * 50)
    
    # Check Django settings
    email_settings = [
        'EMAIL_BACKEND',
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_USE_TLS',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'DEFAULT_FROM_EMAIL',
        'DEBUG'
    ]
    
    print("Django Settings:")
    for setting in email_settings:
        value = getattr(settings, setting, 'NOT SET')
        if setting == 'EMAIL_HOST_PASSWORD':
            display_value = f"SET ({len(str(value))} chars)" if value else "NOT SET"
        else:
            display_value = value
        print(f"  {setting}: {display_value}")
    
    print("\nEnvironment Variables:")
    env_vars = [
        'EMAIL_HOST',
        'EMAIL_PORT', 
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'DEFAULT_FROM_EMAIL',
        'DEBUG'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'NOT SET')
        if var == 'EMAIL_HOST_PASSWORD':
            display_value = f"SET ({len(value)} chars)" if value != 'NOT SET' else "NOT SET"
        else:
            display_value = value
        print(f"  {var}: {display_value}")

def check_render_deployment():
    """Check if we're running on Render"""
    print("\n🚀 Render Deployment Check...")
    print("=" * 50)
    
    render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if render_hostname:
        print(f"✅ Running on Render: {render_hostname}")
        print("🔧 Make sure environment variables are set in Render dashboard")
    else:
        print("📍 Running locally")
        print("🔧 For production, deploy to Render and set environment variables")

def main():
    """Run comprehensive OTP troubleshooting"""
    print("🔍 OTP Email Troubleshooting - Advanced Diagnostics")
    print("=" * 60)
    
    # Check environment
    check_environment()
    
    # Check deployment
    check_render_deployment()
    
    # Test SMTP connection
    smtp_ok = test_smtp_connection()
    
    # Test Django email
    django_ok = test_django_email()
    
    # Test OTP service
    otp_ok = test_otp_service()
    
    # Summary
    print("\n📊 TROUBLESHOOTING SUMMARY")
    print("=" * 60)
    print(f"SMTP Connection: {'✅ OK' if smtp_ok else '❌ FAILED'}")
    print(f"Django Email: {'✅ OK' if django_ok else '❌ FAILED'}")
    print(f"OTP Service: {'✅ OK' if otp_ok else '❌ FAILED'}")
    
    if all([smtp_ok, django_ok, otp_ok]):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ OTP email system should be working")
    else:
        print("\n🔧 ISSUES FOUND - Follow the fixes above")
        
        if not smtp_ok:
            print("🔑 Priority 1: Fix SMTP authentication (Gmail app password)")
        if not django_ok:
            print("📧 Priority 2: Fix Django email configuration")
        if not otp_ok:
            print("🔢 Priority 3: Fix OTP service implementation")

if __name__ == '__main__':
    main()