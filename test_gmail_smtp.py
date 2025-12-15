#!/usr/bin/env python
"""
Test Gmail SMTP connection with your credentials
Run this after updating .env with complete Gmail app password
"""
import smtplib
from decouple import config

def test_gmail_smtp():
    """Test Gmail SMTP connection directly"""
    print("🔐 Testing Gmail SMTP Connection")
    print("=" * 40)
    
    # Get credentials from .env
    email_user = config('EMAIL_HOST_USER', default='')
    email_password = config('EMAIL_HOST_PASSWORD', default='')
    
    print(f"Email: {email_user}")
    print(f"Password length: {len(email_password)} characters")
    
    if len(email_password) < 16:
        print("❌ Gmail app password should be 16 characters!")
        print("🔧 Get new app password from: https://myaccount.google.com/")
        print("   1. Go to Security → 2-Step Verification")
        print("   2. Click 'App passwords'")
        print("   3. Generate new password for 'Mail'")
        print("   4. Copy the 16-character password (like: abcd efgh ijkl mnop)")
        print("   5. Update .env file with complete password")
        return False
    
    try:
        print("📡 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        
        print("🔒 Starting TLS...")
        server.starttls()
        
        print("🔐 Authenticating...")
        server.login(email_user, email_password)
        
        print("✅ SUCCESS! Gmail SMTP connection working!")
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication Failed: {e}")
        print("🔧 Check your Gmail app password")
        return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == '__main__':
    test_gmail_smtp()