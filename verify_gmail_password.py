#!/usr/bin/env python3
"""
Verify Gmail app password step by step
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail_connection():
    print("🔐 GMAIL APP PASSWORD VERIFICATION")
    print("=" * 40)
    
    # Gmail settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email = "simoongalaurent427@gmail.com"
    password = "sghuygvzhowzrdmm"
    
    print(f"📧 Email: {email}")
    print(f"🔑 App Password: {password}")
    print(f"🌐 SMTP Server: {smtp_server}:{smtp_port}")
    
    try:
        print(f"\n🔌 Step 1: Connecting to Gmail SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("✅ Connection established")
        
        print(f"\n🔒 Step 2: Starting TLS encryption...")
        server.starttls()
        print("✅ TLS encryption started")
        
        print(f"\n🔐 Step 3: Authenticating with Gmail...")
        server.login(email, password)
        print("✅ Authentication successful!")
        
        print(f"\n📤 Step 4: Sending test email...")
        
        # Create test email
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = "NRC System - Gmail App Password Test"
        
        body = f"""
Hello!

This is a test email to verify your Gmail app password is working.

✅ Gmail SMTP connection: SUCCESS
✅ Authentication: SUCCESS  
✅ Email sending: SUCCESS

App Password: {password}
Timestamp: {__import__('datetime').datetime.now()}

Your NRC System OTP emails should work perfectly now!

Best regards,
NRC System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server.send_message(msg)
        print("✅ Test email sent successfully!")
        
        server.quit()
        print(f"\n🎉 GMAIL APP PASSWORD IS WORKING PERFECTLY!")
        print(f"📧 Check your email: {email}")
        print(f"🔑 Verified password: {password}")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print(f"\n🔧 TROUBLESHOOTING:")
        print(f"1. 🔑 App password may be incorrect: {password}")
        print(f"2. 🔒 Check if 2FA is enabled on Gmail")
        print(f"3. 🆕 Try generating a new app password")
        print(f"4. ⏰ Wait 5-10 minutes for new password to activate")
        print(f"5. 🌐 Check Gmail security settings")
        return False
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"\n🔧 TROUBLESHOOTING:")
        print(f"1. 🌐 Check internet connection")
        print(f"2. 🔥 Check firewall settings")
        print(f"3. 🏢 Corporate/school networks may block SMTP")
        return False

def gmail_setup_guide():
    print(f"\n📋 GMAIL APP PASSWORD SETUP GUIDE")
    print("=" * 40)
    print(f"1. 🌐 Go to: https://myaccount.google.com/security")
    print(f"2. 🔒 Enable 2-Step Verification (if not enabled)")
    print(f"3. 🔑 Go to App Passwords section")
    print(f"4. 📱 Select 'Mail' and 'Other (custom name)'")
    print(f"5. 📝 Enter 'NRC System' as the name")
    print(f"6. 🎯 Copy the generated 16-character password")
    print(f"7. 🔄 Replace the password in .env file")
    print(f"8. ⏰ Wait 5-10 minutes for activation")
    print(f"9. 🧪 Run this test again")

if __name__ == "__main__":
    success = test_gmail_connection()
    
    if not success:
        gmail_setup_guide()
        
        print(f"\n🎯 QUICK FIX OPTIONS:")
        print(f"1. 🔄 Generate new app password and update .env")
        print(f"2. ⏰ Wait 10 minutes if password is new")
        print(f"3. 🌐 Try different internet connection")
        print(f"4. 📞 Contact Gmail support if issues persist")
    else:
        print(f"\n🚀 READY FOR OTP TESTING!")
        print(f"   Run: python manage.py runserver")
        print(f"   Go to: http://localhost:8000/accounts/login/")
        print(f"   Test OTP login flow")