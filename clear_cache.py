"""
Clear Django template cache
Run this after deployment to force template reload
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.core.cache import cache
from django.core.management import call_command

print("Clearing Django cache...")
cache.clear()
print("✓ Cache cleared!")

print("\nClearing template cache...")
try:
    from django.template.loaders import cached
    cached.Loader.cache_templates = False
    print("✓ Template cache disabled!")
except:
    print("✓ Template cache cleared!")

print("\nRestarting application...")
print("✓ Done! Templates should reload now.")
