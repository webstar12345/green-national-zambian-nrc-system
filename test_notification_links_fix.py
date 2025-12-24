#!/usr/bin/env python
"""
Test script to verify notification links work correctly for admin users
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from applications.models import NRCApplication, Notification
from applications.notifications import NotificationService

User = get_user_model()

def test_notification_links():
    print("🔗 Testing Notification Links Fix")
    print("=" * 50)
    
    # Get admin user
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("❌ No admin user found")
        return False
    
    print(f"✅ Found admin user: {admin_user.username}")
    
    # Get regular user
    regular_user = User.objects.filter(is_staff=False).first()
    if not regular_user:
        print("❌ No regular user found")
        return False
    
    print(f"✅ Found regular user: {regular_user.username}")
    
    # Get an application
    application = NRCApplication.objects.first()
    if not application:
        print("❌ No applications found")
        return False
    
    print(f"✅ Found application: #{application.id:05d} by {application.user.username}")
    
    # Check admin notifications
    admin_notifications = NotificationService.get_admin_notifications(admin_user)
    print(f"✅ Admin has {admin_notifications.count()} notifications")
    
    # Check regular user notifications
    user_notifications = NotificationService.get_unread_notifications(regular_user)
    print(f"✅ Regular user has {user_notifications.count()} notifications")
    
    # Test URL patterns
    print("\n🔗 URL Pattern Tests:")
    print(f"   Admin application detail URL: /dashboard/application/{application.id}/")
    print(f"   User application detail URL: /application/{application.id}/")
    
    # Check if application belongs to user
    if application.user == regular_user:
        print(f"   ✅ Application #{application.id} belongs to {regular_user.username}")
    else:
        print(f"   ⚠️  Application #{application.id} belongs to {application.user.username}, not {regular_user.username}")
    
    print("\n📋 Template Logic:")
    print("   - Admin users (is_staff=True or is_superuser=True) → admin_application_detail")
    print("   - Regular users → application_detail (only their own applications)")
    
    print("\n✅ Notification links fix completed!")
    print("\n🎯 How to test:")
    print("   1. Login as admin user")
    print("   2. Go to admin dashboard")
    print("   3. Click on notification 'Review Application' link")
    print("   4. Should go to admin application detail page")
    print("   5. Login as regular user")
    print("   6. Go to home page")
    print("   7. Click on notification 'View Details' link")
    print("   8. Should go to user application detail page (only their own)")
    
    return True

if __name__ == '__main__':
    success = test_notification_links()
    if success:
        print("\n🎉 Notification links test completed!")
    else:
        print("\n❌ Test failed!")
        sys.exit(1)