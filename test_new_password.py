#!/usr/bin/env python3
"""
Quick test of the new Gmail app password
"""
import smtplib

def test_new_gmail_password():
    """Test the new Gmail app password"""
    email = "simoongalaurent427@gmail.com"
    new_password = "uroaoegylbpusjfy"
    
    print("🧪 Testing New Gmail App Password")
    print("=" * 40)
    print(f"📧 Email: {email}")
    print(f"🔑 Password length: {len(new_password)} characters")
    
    try:
        # Test Gmail SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, new_password)
        server.quit()
        
        print("✅ SUCCESS! New Gmail app password is working!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("🔧 The new app password may not be activated yet")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_new_gmail_password()