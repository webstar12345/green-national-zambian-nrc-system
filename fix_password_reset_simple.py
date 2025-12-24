#!/usr/bin/env python
"""
Fix Password Reset Domain Issue - Simple Approach
Delete all sites and create a fresh localhost:8000 site
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.sites.models import Site
from decouple import config

def fix_password_reset_simple():
    """Fix the site domain - simple approach"""
    print("🔧 Fixing Password Reset Domain Issue (Simple)...")
    print("=" * 50)
    print()
    
    try:
        # List all existing sites
        sites = Site.objects.all()
        print(f"Found {sites.count()} existing sites:")
        for site in sites:
            print(f"  ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
        print()
        
        # Delete all existing sites
        print("🗑️ Deleting all existing sites...")
        Site.objects.all().delete()
        print("✅ All sites deleted")
        
        # Check if we're in development
        debug_mode = config('DEBUG', default=True, cast=bool)
        
        if debug_mode:
            target_domain = 'localhost:8000'
            target_name = 'NRC System (Development)'
            print("🔧 Development mode - creating localhost:8000 site")
        else:
            target_domain = config('SITE_DOMAIN', default='green-national-zambian-nrc-system.onrender.com')
            target_name = 'Zambian NRC System'
            print("🚀 Production mode - creating production site")
        
        # Create new site with ID=1
        site = Site.objects.create(pk=1, domain=target_domain, name=target_name)
        print(f"✅ Created new site: {target_domain} (ID: {site.id})")
        
        print()
        print(f"✅ Final site configuration:")
        print(f"   ID: {site.id}")
        print(f"   Domain: {site.domain}")
        print(f"   Name: {site.name}")
        print()
        
        print("🔗 Password reset links will now use:")
        if debug_mode:
            print(f"   http://{site.domain}/accounts/password/reset/confirm/...")
        else:
            print(f"   https://{site.domain}/accounts/password/reset/confirm/...")
        print()
        
        print("📧 Test password reset:")
        print("1. Go to: http://localhost:8000/accounts/password/reset/")
        print("2. Enter your email address")
        print("3. Check email for reset link")
        print("4. Link should now point to localhost:8000")
        print()
        
        print("✅ Password reset domain fix complete!")
        
    except Exception as e:
        print(f"❌ Error fixing domain: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_password_reset_simple()