#!/usr/bin/env python3
"""
Force Gmail configuration in Django settings
"""
import os
from pathlib import Path

def force_gmail_settings():
    print("🔧 FORCING GMAIL CONFIGURATION IN DJANGO")
    print("=" * 45)
    
    settings_file = Path('nrc_system/settings.py')
    
    if not settings_file.exists():
        print("❌ Settings file not found!")
        return False
    
    # Read current settings
    content = settings_file.read_text()
    
    # Gmail configuration to inject
    gmail_config = '''
# FORCED GMAIL CONFIGURATION FOR OTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'simoongalaurent427@gmail.com'
EMAIL_HOST_PASSWORD = 'sghuygvzhowzrdmm'
DEFAULT_FROM_EMAIL = 'simoongalaurent427@gmail.com'

# Override any existing email configuration
import os
os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'simoongalaurent427@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'sghuygvzhowzrdmm'
os.environ['DEFAULT_FROM_EMAIL'] = 'simoongalaurent427@gmail.com'
'''
    
    # Check if already added
    if 'FORCED GMAIL CONFIGURATION' in content:
        print("✅ Gmail configuration already forced in settings")
        return True
    
    # Add Gmail configuration at the end
    content += gmail_config
    
    # Write back to file
    settings_file.write_text(content)
    
    print("✅ Gmail configuration forced in Django settings")
    print("📧 Email settings:")
    print("   HOST: smtp.gmail.com")
    print("   PORT: 587")
    print("   USER: simoongalaurent427@gmail.com")
    print("   PASSWORD: sghuygvzhowzrdmm")
    
    return True

if __name__ == "__main__":
    success = force_gmail_settings()
    
    if success:
        print(f"\n🎉 GMAIL FORCED IN DJANGO!")
        print(f"   - Django will now use Gmail SMTP directly")
        print(f"   - OTP emails will be sent to your Gmail")
        print(f"   - No more fallback messages")
        print(f"\n🚀 Next steps:")
        print(f"   1. Restart Django server")
        print(f"   2. Test login - real emails will be sent!")
        print(f"   3. Check simoongalaurent427@gmail.com for OTP")
    else:
        print(f"\n❌ Failed to force Gmail configuration")
        print(f"   Check if settings.py file exists")