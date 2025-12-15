#!/usr/bin/env python
"""
Test if .env file is being loaded correctly
"""
import os
from decouple import config

print("🔍 Testing .env File Loading")
print("=" * 40)

# Test direct file reading
print("📄 Direct .env file check:")
try:
    with open('.env', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'EMAIL_HOST_PASSWORD' in line:
                print(f"   Found in file: {line.strip()}")
                break
except FileNotFoundError:
    print("   ❌ .env file not found!")

# Test decouple config loading
print("\n🔧 Decouple config loading:")
email_password = config('EMAIL_HOST_PASSWORD', default='NOT_FOUND')
email_host = config('EMAIL_HOST', default='NOT_FOUND')
email_user = config('EMAIL_HOST_USER', default='NOT_FOUND')

print(f"   EMAIL_HOST: {email_host}")
print(f"   EMAIL_HOST_USER: {email_user}")
print(f"   EMAIL_HOST_PASSWORD: {'SET' if email_password != 'NOT_FOUND' else 'NOT_FOUND'} ({len(email_password)} chars)")

# Test os.environ
print("\n🌍 OS Environment variables:")
print(f"   EMAIL_HOST: {os.environ.get('EMAIL_HOST', 'NOT_SET')}")
print(f"   EMAIL_HOST_USER: {os.environ.get('EMAIL_HOST_USER', 'NOT_SET')}")
print(f"   EMAIL_HOST_PASSWORD: {'SET' if os.environ.get('EMAIL_HOST_PASSWORD') else 'NOT_SET'}")

# Test Django settings loading
print("\n⚙️  Django settings test:")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
import django
django.setup()

from django.conf import settings

print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"   EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'NOT_SET')}")
print(f"   EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'NOT_SET')}")
print(f"   EMAIL_HOST_PASSWORD: {'SET' if getattr(settings, 'EMAIL_HOST_PASSWORD', '') else 'NOT_SET'}")
print(f"   DEBUG: {settings.DEBUG}")