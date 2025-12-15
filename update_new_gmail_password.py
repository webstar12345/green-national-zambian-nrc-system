#!/usr/bin/env python3
"""
Update and test new Gmail app password
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

def update_and_test_gmail():
    print("🔑 UPDATING NEW GMAIL APP PASSWORD")
    print("=" * 50)
    
    new_password = "sghuygvzhowzrdmm"
    
    # Update local .env file
    env_file = Path('.env')
    if env_file.exists():
        content = env_file.read_text()
        
        # Replace old password with new one
        if 'EMAIL_HOST_PASSWORD=' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('EMAIL_HOST_PASSWORD='):
                    lines[i] = f'EMAIL_HOST_PASSWORD={new_password}'
                    break
            
            env_file.write_text('\n'.join(lines))
            print(f"✅ Updated local .env file with new password")
        else:
            # Add password if not exists
            with open('.env', 'a') as f:
                f.write(f'\nEMAIL_HOST_PASSWORD={new_password}\n')
            print(f"✅ Added new password to .env file")
    
    # Test the new password
    print(f"\n🧪 Testing new Gmail app password: {new_password}")
    
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        # Override settings for testing
        settings.EMAIL_HOST_PASSWORD = new_password
        
        result = send_mail(
            subject='NRC System - New Password Test',
            message=f'''
Hello!

This is a test email using the new Gmail app password: {new_password}

If you receive this email, the new password is working correctly!

Time: {django.utils.timezone.now()}

Best regards,
NRC System
            ''',
            from_email='simoongalaurent427@gmail.com',
            recipient_list=['simoongalaurent427@gmail.com'],
            fail_silently=False,
        )
        
        if result == 1:
            print("✅ NEW PASSWORD WORKS! Test email sent successfully!")
            print("📧 Check your email inbox for confirmation")
            
            print(f"\n🎯 NEXT STEPS:")
            print(f"1. Update Render.com environment variable:")
            print(f"   EMAIL_HOST_PASSWORD = {new_password}")
            print(f"2. Wait 2-3 minutes for deployment")
            print(f"3. Test OTP login on production site")
            
            return True
        else:
            print("❌ Email sending failed - result was 0")
            return False
            
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        
        if "authentication failed" in str(e).lower():
            print("🔐 The new app password may be incorrect or not activated yet")
            print("   - Double-check the password: sghuygvzhowzrdmm")
            print("   - Wait a few minutes for Gmail to activate it")
            print("   - Try generating another app password if needed")
        
        return False

if __name__ == "__main__":
    success = update_and_test_gmail()
    
    if success:
        print("\n🎉 READY FOR PRODUCTION DEPLOYMENT!")
        print("   Update Render.com with the new password and test OTP login")
    else:
        print("\n🚨 PASSWORD NEEDS VERIFICATION")
        print("   Check Gmail app password generation and try again")