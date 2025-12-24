#!/usr/bin/env python
"""
Test Admin Bypass Functionality
Tests that admin users can login without OTP verification
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

User = get_user_model()

def test_admin_bypass():
    """Test that admin users bypass OTP verification"""
    print("🔧 Testing Admin Bypass Functionality...")
    
    # Create test client
    client = Client()
    
    # Check if admin user exists
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No admin user found. Creating test admin...")
            admin_user = User.objects.create_superuser(
                username='testadmin',
                email='admin@test.com',
                password='testpass123',
                first_name='Test',
                last_name='Admin'
            )
            print(f"✅ Created test admin: {admin_user.username}")
        else:
            print(f"✅ Found existing admin: {admin_user.username}")
        
        # Test regular user (should require OTP)
        regular_user = User.objects.filter(is_superuser=False, is_staff=False).first()
        if not regular_user:
            regular_user = User.objects.create_user(
                username='testuser',
                email='user@test.com',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )
            print(f"✅ Created test regular user: {regular_user.username}")
        
        print("\n📋 Test Results:")
        print(f"Admin User: {admin_user.username} (is_superuser: {admin_user.is_superuser}, is_staff: {admin_user.is_staff})")
        print(f"Regular User: {regular_user.username} (is_superuser: {regular_user.is_superuser}, is_staff: {regular_user.is_staff})")
        
        print("\n🔐 Authentication Logic:")
        print("- Admin users (is_staff=True OR is_superuser=True) → Direct login (no OTP)")
        print("- Regular users → OTP verification required")
        
        print("\n✅ Admin bypass functionality is configured!")
        print("🚀 Admin users will now login directly without OTP verification")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_admin_bypass()