#!/usr/bin/env python
"""
Fix Password Reset Domain Issue
Updates the Django Sites framework to use localhost for development
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.sites.models import Site
from decouple import config

def fix_password_reset_domain():
    """Fix the site domain for password reset emails"""
    print("🔧 Fixing Password Reset Domain Issue...")
    print("=" * 50)
    print()
    
    try:
        # Get current site
        site = Site.objects.get_current()
        print(f"Current site domain: {site.domain}")
        print(f"Current site name: {site.name}")
        print()
        
        # Check if we're in development
        debug_mode = config('DEBUG', default=True, cast=bool)
        site_domain = config('SITE_DOMAIN', default='localhost:8000')
        
        if debug_mode:
            # Development mode - use localhost
            new_domain = 'localhost:8000'
            new_name = 'NRC System (Development)'
            print("🔧 Development mode detected")
        else:
            # Production mode - use configured domain
            new_domain = site_domain
            new_name = 'Zambian NRC System'
            print("🚀 Production mode detected")
        
        # Update site
        site.domain = new_domain
        site.name = new_name
        site.save()
        
        print(f"✅ Updated site domain to: {new_domain}")
        print(f"✅ Updated site name to: {new_name}")
        print()
        
        print("🔗 Password reset links will now use:")
        print(f"   http://{new_domain}/accounts/password/reset/confirm/...")
        print()
        
        print("📧 Test password reset:")
        print("1. Go to: http://localhost:8000/accounts/password/reset/")
        print("2. Enter your email address")
        print("3. Check email for reset link")
        print("4. Link should now point to localhost:8000")
        
    except Exception as e:
        print(f"❌ Error fixing domain: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_password_reset_domain()