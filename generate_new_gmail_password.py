#!/usr/bin/env python3
"""
Gmail App Password Generator Helper
URGENT: Use this to generate a new Gmail app password after security breach
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText

def print_instructions():
    """Print step-by-step instructions for creating NEW Gmail app password"""
    print("🚨 URGENT: Gmail App Password Security Fix")
    print("=" * 50)
    print()
    print("⚠️  Your old password was EXPOSED in GitHub!")
    print("⚠️  Gmail may have disabled it for security!")
    print()
    print("🔒 IMMEDIATE STEPS:")
    print()
    print("1. Go to Google Account settings:")
    print("   https://myaccount.google.com/")
    print()
    print("2. Click 'Security' → '2-Step Verification'")
    print()
    print("3. Scroll to 'App passwords'")
    print()
    print("4. 🗑️  DELETE the old app password:")
    print("   - Look for 'NRC System' or similar")
    print("   - Click the trash/delete icon")
    print("   - Confirm deletion")
    print()
    print("5. ➕ CREATE NEW app password:")
    print("   - Click 'Select app' → 'Mail'")
    print("   - Click 'Select device' → 'Other (Custom name)'")
    print("   - Type: 'NRC System SECURE'")
    print("   - Click 'Generate'")
    print()
    print("6. 📋 COPY the new 16-character password")
    print("   (Format: abcd efgh ijkl mnop)")
    print()
    print("7. ✅ REMOVE SPACES and use in .env file")
    print()
    print("🔥 CRITICAL: The old password 'feirlikfycpiddbw' is COMPROMISED!")
    print()

def test_new_password():
    """Test the new Gmail app password"""
    print("🧪 Testing New Gmail App Password")
    print("=" * 40)
    
    email = input("Enter your Gmail address (simoongalaurent427@gmail.com): ").strip()
    if not email:
        email = "simoongalaurent427@gmail.com"
    
    new_password = input("Enter your NEW 16-character app password: ").strip()
    
    if len(new_password) != 16:
        print("❌ Gmail app passwords should be exactly 16 characters!")
        print("   Make sure you removed all spaces!")
        return False
    
    try:
        print(f"📧 Testing connection for: {email}")
        print(f"🔑 Password length: {len(new_password)} characters")
        
        # Test Gmail SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, new_password)
        server.quit()
        
        print("✅ SUCCESS! New Gmail app password is working!")
        print()
        print("📝 Next steps:")
        print("1. Update your .env file with this new password")
        print("2. Update production environment variables on Render.com")
        print("3. Test OTP emails in production")
        print()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("🔧 The new app password is incorrect or not activated yet")
        print("💡 Wait 1-2 minutes and try again")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def update_env_file():
    """Help update the .env file with new password"""
    print("📝 Updating .env File")
    print("=" * 30)
    
    email = input("Enter your Gmail address: ").strip()
    new_password = input("Enter your NEW app password: ").strip()
    
    if len(new_password) != 16:
        print("❌ Invalid password length!")
        return
    
    env_content = f"""# Email Configuration - UPDATED FOR SECURITY
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER={email}
EMAIL_HOST_PASSWORD={new_password}
DEFAULT_FROM_EMAIL={email}
"""
    
    print("📋 Add these lines to your .env file:")
    print("-" * 40)
    print(env_content)
    print("-" * 40)
    print()
    print("🚀 Production Environment Variables:")
    print(f"EMAIL_HOST_USER={email}")
    print(f"EMAIL_HOST_PASSWORD={new_password}")
    print("EMAIL_HOST=smtp.gmail.com")
    print("EMAIL_PORT=587")
    print("EMAIL_USE_TLS=True")
    print(f"DEFAULT_FROM_EMAIL={email}")

def main():
    """Main function"""
    print("🚨 GMAIL SECURITY BREACH - IMMEDIATE ACTION REQUIRED")
    print("=" * 60)
    print()
    
    while True:
        print("Choose an option:")
        print("1. 📖 Show instructions for new app password")
        print("2. 🧪 Test new app password")
        print("3. 📝 Generate .env file content")
        print("4. 🚪 Exit")
        print()
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == '1':
            print_instructions()
            input("\nPress Enter when you have generated your new app password...")
        elif choice == '2':
            if test_new_password():
                print("🎉 Password test successful! You can now update production.")
            else:
                print("❌ Password test failed. Please generate a new one.")
        elif choice == '3':
            update_env_file()
        elif choice == '4':
            print("👋 Remember to:")
            print("1. Update production environment variables")
            print("2. Test OTP emails")
            print("3. Clean Git history")
            break
        else:
            print("❌ Invalid choice!")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()