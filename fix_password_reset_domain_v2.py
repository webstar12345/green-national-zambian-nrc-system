#!/usr/bin/env python
"""
Fix Password Reset Domain Issue - Version 2
Properly handles existing sites and updates domain for localhost
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.sites.models import Site
from decouple import config

def fix_password_reset_domain_v2():
    """Fix the site domain for password reset emails - handles duplicates"""
    print("🔧 Fixing Password Reset Domain Issue (v2)...")
    print("=" * 50)
    print()
    
    try:
        # List all existing sites
        sites = Site.objects.all()
        print(f"Found {sites.count()} existing sites:")
        for site in sites:
            print(f"  ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
        print()
        
        # Check if we're in development
        debug_mode = config('DEBUG', default=True, cast=bool)
        
        if debug_mode:
            # Development mode - ensure localhost:8000
            target_domain = 'localhost:8000'
            target_name = 'NRC System (Development)'
            print("🔧 Development mode - setting up localhost:8000")
        else:
            # Production mode
            target_domain = config('SITE_DOMAIN', default='green-national-zambian-nrc-system.onrender.com')
            target_name = 'Zambian NRC System'
            print("🚀 Production mode - using configured domain")
        
        # Find or create the site with ID=1 (Django's default)
        try:
            site = Site.objects.get(pk=1)
            print(f"Found existing site with ID=1: {site.domain}")
            
            # Update the existing site
            site.domain = target_domain
            site.name = target_name
            site.save()
            print(f"✅ Updated existing site to: {target_domain}")
            
        except Site.DoesNotExist:
            # Create new site with ID=1
            site = Site.objects.create(pk=1, domain=target_domain, name=target_name)
            print(f"✅ Created new site: {target_domain}")
        
        # Remove any duplicate sites with the same domain (but different IDs)
        duplicates = Site.objects.filter(domain=target_domain).exclude(pk=site.pk)
        if duplicates.exists():
            print(f"🧹 Removing {duplicates.count()} duplicate sites...")
            duplicates.delete()
        
        print()
        print(f"✅ Site configuration complete!")
        print(f"   Domain: {site.domain}")
        print(f"   Name: {site.name}")
        print(f"   ID: {site.id}")
        print()
        
        print("🔗 Password reset links will now use:")
        if debug_mode:
            print(f"   http://{target_domain}/accounts/password/reset/confirm/...")
        else:
            print(f"   https://{target_domain}/accounts/password/reset/confirm/...")
        print()
        
        print("📧 Test password reset:")
        print("1. Go to: http://localhost:8000/accounts/password/reset/")
        print("2. Enter your email address")
        print("3. Check email for reset link")
        print("4. Link should now point to the correct domain")
        
    except Exception as e:
        print(f"❌ Error fixing domain: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_password_reset_domain_v2()