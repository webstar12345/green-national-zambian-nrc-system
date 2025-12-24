#!/usr/bin/env python
"""
Emergency fix for Render database connection issues
Diagnoses and fixes PostgreSQL connection problems on Render
"""

import os
import sys
from urllib.parse import urlparse

def diagnose_database_connection():
    """Diagnose database connection issues"""
    print("🔍 DIAGNOSING RENDER DATABASE CONNECTION ISSUE")
    print("=" * 60)
    
    # Check environment variables
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not found!")
        print("\n🔧 SOLUTION:")
        print("1. Go to your Render dashboard")
        print("2. Navigate to your PostgreSQL service")
        print("3. Copy the 'External Database URL'")
        print("4. Add it as DATABASE_URL environment variable in your web service")
        return False
    
    print(f"✅ DATABASE_URL found: {database_url[:50]}...")
    
    # Parse the database URL
    try:
        parsed = urlparse(database_url)
        print(f"\n📊 Database Connection Details:")
        print(f"   Host: {parsed.hostname}")
        print(f"   Port: {parsed.port}")
        print(f"   Database: {parsed.path[1:] if parsed.path else 'N/A'}")
        print(f"   Username: {parsed.username}")
        
        # Check if it's an internal or external URL
        if parsed.hostname and 'dpg-' in parsed.hostname:
            if parsed.hostname.endswith('-a'):
                print("✅ Using external database URL (correct for web service)")
            else:
                print("⚠️  Using internal database URL - this might cause issues")
                print("   Try using the external URL ending with '-a'")
        
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        return False
    
    return True

def generate_database_fix():
    """Generate database connection fix"""
    print("\n🛠️  RENDER DATABASE CONNECTION FIX")
    print("=" * 60)
    
    print("\n1. CHECK YOUR RENDER DASHBOARD:")
    print("   • Go to https://dashboard.render.com")
    print("   • Navigate to your PostgreSQL service")
    print("   • Copy the 'External Database URL'")
    
    print("\n2. UPDATE WEB SERVICE ENVIRONMENT:")
    print("   • Go to your web service settings")
    print("   • Add/Update environment variable:")
    print("     Key: DATABASE_URL")
    print("     Value: [Your External Database URL]")
    
    print("\n3. VERIFY DATABASE URL FORMAT:")
    print("   Should look like:")
    print("   postgresql://user:password@dpg-xxxxx-a/database_name")
    print("   Note the '-a' at the end of the hostname!")
    
    print("\n4. COMMON ISSUES & SOLUTIONS:")
    print("   • Using internal URL instead of external")
    print("   • Database service not running")
    print("   • Incorrect environment variable name")
    print("   • Network connectivity issues")
    
    print("\n5. IMMEDIATE ACTIONS:")
    print("   • Restart your web service after updating DATABASE_URL")
    print("   • Check database service status")
    print("   • Verify environment variables are saved")

def create_emergency_settings():
    """Create emergency settings with better error handling"""
    
    settings_content = '''
# Emergency database connection settings for Render
import os
import dj_database_url
from decouple import config

# Database configuration with better error handling
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    # Fallback for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Connection pool settings for PostgreSQL
if 'postgresql' in DATABASE_URL:
    DATABASES['default'].update({
        'OPTIONS': {
            'MAX_CONNS': 20,
            'OPTIONS': {
                'MAX_CONNS': 20,
            }
        },
        'CONN_MAX_AGE': 600,
    })

# Add connection retry logic
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 30,
    'options': '-c default_transaction_isolation=serializable'
}
'''
    
    with open('emergency_database_settings.py', 'w') as f:
        f.write(settings_content)
    
    print("\n📄 Created emergency_database_settings.py")
    print("   You can reference this for proper database configuration")

def main():
    """Main diagnostic and fix function"""
    print("🚨 RENDER DATABASE CONNECTION EMERGENCY FIX")
    print("=" * 60)
    
    # Run diagnostics
    connection_ok = diagnose_database_connection()
    
    # Generate fix instructions
    generate_database_fix()
    
    # Create emergency settings
    create_emergency_settings()
    
    print("\n" + "=" * 60)
    print("🎯 QUICK FIX CHECKLIST:")
    print("=" * 60)
    print("□ 1. Get External Database URL from Render PostgreSQL service")
    print("□ 2. Update DATABASE_URL environment variable in web service")
    print("□ 3. Ensure URL ends with '-a' (external connection)")
    print("□ 4. Restart web service")
    print("□ 5. Check database service is running")
    print("□ 6. Verify environment variables are saved")
    
    print("\n🔗 USEFUL LINKS:")
    print("• Render Dashboard: https://dashboard.render.com")
    print("• Render Docs: https://render.com/docs/databases")
    
    if not connection_ok:
        print("\n❌ Database connection issues detected!")
        print("Follow the steps above to resolve the issue.")
        return False
    else:
        print("\n✅ Database configuration appears correct.")
        print("If you're still having issues, check Render service status.")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)