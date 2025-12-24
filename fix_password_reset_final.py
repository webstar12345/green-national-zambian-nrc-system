#!/usr/bin/env python
"""
Fix Password Reset Domain Issue - Final Version
Properly handles existing sites and ensures localhost:8000 is the current site
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.sites.models import Site
from decouple import config

def fix_password_reset_final():
    """Fix the site domain for password reset emails - final solution"""
    print("🔧 Fixing Password Reset Domain Issue (Final)...")
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
            target_domain = 'localhost:8000'
            target_name = 'NRC System (Development)'
            print("🔧 Development mode - ensuring localhost:8000 is the current site")
        else:
            target_domain = config('SITE_DOMAIN', default='green-national-zambian-nrc-system.onrender.com')
            target_name = 'Zambian NRC System'
            print("🚀 Production mode - using configured domain")
        
        # Find the site with the target domain
        localhost_site = None
        try:
            localhost_site = Site.objects.get(domain=target_domain)
            print(f"Found existing site with target domain: ID={localhost_site.id}")
        except Site.DoesNotExist:
            print("No site found with target domain")
        except Site.MultipleObjectsReturned:
            # Multiple sites with same domain - get the first one
            localhost_site = Site.objects.filter(domain=target_domain).first()
            print(f"Multiple sites found, using first: ID={localhost_site.id}")
        
        if localhost_site:
            # Update the existing localhost site to be the current site (ID=1)
            current_site = None
            try:
                current_site = Site.objects.get(pk=1)
                print(f"Current site (ID=1): {current_site.domain}")
                
                if current_site.id != localhost_site.id:
                    # Swap the IDs - make localhost site the current site
                    print("🔄 Swapping site configurations...")
                    
                    # Temporarily change current site to avoid conflicts
                    temp_domain = f"temp-{current_site.domain}"
                    current_site.domain = temp_domain
                    current_site.save()
                    
                    # Update localhost site to be ID=1
                    localhost_site.pk = 1
                    localhost_site.domain = target_domain
                    localhost_site.name = target_name
                    localhost_site.save()
                    
                    # Delete the old current site
                    Site.objects.filter(domain=temp_domain).delete()
                    
                    print(f"✅ Made {target_domain} the current site (ID=1)")
                else:
                    # Already the current site, just update name
                    current_site.name = target_name
                    current_site.save()
                    print(f"✅ Updated current site name")
                    
            except Site.DoesNotExist:
                # No current site, make localhost site ID=1
                localhost_site.pk = 1
                localhost_site.domain = target_domain
                localhost_site.name = target_name
                localhost_site.save()
                print(f"✅ Made {target_domain} the current site (ID=1)")
        else:
            # No localhost site exists, create or update ID=1
            try:
                current_site = Site.objects.get(pk=1)
                current_site.domain = target_domain
                current_site.name = target_name
                current_site.save()
                print(f"✅ Updated current site to {target_domain}")
            except Site.DoesNotExist:
                Site.objects.create(pk=1, domain=target_domain, name=target_name)
                print(f"✅ Created new current site: {target_domain}")
        
        # Clean up any duplicate sites
        duplicates = Site.objects.filter(domain=target_domain).exclude(pk=1)
        if duplicates.exists():
            print(f"🧹 Removing {duplicates.count()} duplicate sites...")
            duplicates.delete()
        
        # Verify final state
        final_site = Site.objects.get(pk=1)
        print()
        print(f"✅ Final site configuration:")
        print(f"   ID: {final_site.id}")
        print(f"   Domain: {final_site.domain}")
        print(f"   Name: {final_site.name}")
        print()
        
        print("🔗 Password reset links will now use:")
        if debug_mode:
            print(f"   http://{final_site.domain}/accounts/password/reset/confirm/...")
        else:
            print(f"   https://{final_site.domain}/accounts/password/reset/confirm/...")
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
    fix_password_reset_final()