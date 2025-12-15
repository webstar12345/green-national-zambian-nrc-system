#!/usr/bin/env python3
"""
Quick test to check if Gmail app password is working
"""
import smtplib
from email.mime.text import MIMEText

def test_gmail_password():
    print("🔐 TESTING GMAIL APP PASSWORD")
    print("=" * 40)
    
    # Your current credentials
    email = "simoongalaurent427@gmail.com"
    password = "sghuygvzhowzrdmm"
    
    print(f"📧 Testing email: {email}")
    print(f"🔑 Testing password: {password[:4]}***{password[-4:]}")
    
    try:
        # Test SMTP connection
        print("\n🔌 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("🔐 Attempting authentication...")
        server.login(email, password)
        
        print("✅ SUCCESS! Gmail app password is ACTIVE and working!")
        
        # Send test email
        print("📤 Sending test email...")
        msg = MIMEText("Test email from NRC system - Gmail app password is working!")
        msg['Subject'] = 'Gmail App Password Test - SUCCESS'
        msg['From'] = email
        msg['To'] = email
        
        server.send_message(msg)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print("📬 Check your inbox for the test email")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("❌ AUTHENTICATION FAILED!")
        print(f"   Error: {e}")
        print("\n🔍 DIAGNOSIS:")
        print("   - Gmail app password is DEACTIVATED or INCORRECT")
        print("   - Need to generate a new app password")
        return False
        
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")
        print("\n🔍 POSSIBLE CAUSES:")
        print("   - Network connectivity issues")
        print("   - SMTP port blocked")
        print("   - Gmail server issues")
        return False

if __name__ == "__main__":
    success = test_gmail_password()
    
    if not success:
        print("\n🛠️ NEXT STEPS:")
        print("1. Go to Gmail → Manage Account → Security")
        print("2. Navigate to 2-Step Verification → App passwords")
        print("3. Generate a new app password")
        print("4. Update Render.com environment variables")
        print("5. Test again")
    else:
        print("\n🎉 Gmail configuration is working!")
        print("   The issue might be elsewhere in the Django setup")