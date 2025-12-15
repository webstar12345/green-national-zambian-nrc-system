#!/usr/bin/env python3
"""
Gmail App Password Setup Helper
This script helps you generate and test a new Gmail app password for OTP emails.
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def print_instructions():
    """Print step-by-step instructions for creating Gmail app password"""
    print("🔐 Gmail App Password Setup Instructions")
    print("=" * 50)
    print()
    print("1. Go to your Google Account settings:")
    print("   https://myaccount.google.com/")
    print()
    print("2. Click 'Security' in the left sidebar")
    print()
    print("3. Under 'Signing in to Google', click '2-Step Verification'")
    print("   (You MUST have 2FA enabled first)")
    print()
    print("4. Scroll down and click 'App passwords'")
    print()
    print("5. Click 'Select app' and choose 'Mail'")
    print()
    print("6. Click 'Select device' and choose 'Other (Custom name)'")
    print()
    print("7. Type 'NRC System' as the name")
    print()
    print("8. Click 'Generate'")
    print()
    print("9. Copy the 16-character password (it looks like: abcd efgh ijkl mnop)")
    print()
    print("10. Remove the spaces and use it in your .env file")
    print()

def test_gmail_connection(email, password):
    """Test Gmail SMTP connection with provided credentials"""
    try:
        print(f"📧 Testing connection for: {email}")
        print(f"🔑 Password length: {len(password)} characters")
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.quit()
        
        print("✅ Gmail SMTP connection successful!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("🔧 Your Gmail app password is incorrect or expired")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def update_env_file(new_password):
    """Update the .env file with new Gmail app password"""
    try:
        # Read current .env file
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update the EMAIL_HOST_PASSWORD line
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('EMAIL_HOST_PASSWORD='):
                lines[i] = f'EMAIL_HOST_PASSWORD={new_password}\n'
                updated = True
                break
        
        if updated:
            # Write back to .env file
            with open('.env', 'w') as f:
                f.writelines(lines)
            print("✅ .env file updated successfully!")
            return True
        else:
            print("❌ Could not find EMAIL_HOST_PASSWORD in .env file")
            return False
            
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def main():
    """Main function"""
    print("🔐 Gmail App Password Fix Tool")
    print("=" * 40)
    print()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        return
    
    # Get current email from .env
    current_email = None
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('EMAIL_HOST_USER='):
                    current_email = line.split('=', 1)[1].strip()
                    break
    except:
        pass
    
    if not current_email:
        print("❌ Could not find EMAIL_HOST_USER in .env file")
        return
    
    print(f"📧 Current email: {current_email}")
    print()
    
    # Show instructions
    choice = input("Do you need instructions for creating a Gmail app password? (y/n): ").lower()
    if choice == 'y':
        print_instructions()
        input("Press Enter when you have your new app password...")
    
    # Get new app password
    print()
    new_password = input("Enter your new Gmail app password (16 characters, no spaces): ").strip()
    
    if len(new_password) != 16:
        print("❌ Gmail app passwords should be exactly 16 characters")
        return
    
    # Test the new password
    print()
    print("🧪 Testing new Gmail app password...")
    if test_gmail_connection(current_email, new_password):
        # Update .env file
        if update_env_file(new_password):
            print()
            print("🎉 Gmail app password updated successfully!")
            print("✅ OTP emails should now work properly")
        else:
            print("❌ Failed to update .env file")
    else:
        print("❌ New password test failed. Please check your credentials.")

if __name__ == "__main__":
    main()