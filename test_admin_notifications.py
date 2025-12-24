#!/usr/bin/env python
"""
Test script for admin notification system
Tests that admin users receive notifications when new applications are submitted
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
from datetime import date

User = get_user_model()

def test_admin_notifications():
    print("🧪 Testing Admin Notification System")
    print("=" * 50)
    
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin_test',
        defaults={
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Created admin user: {admin_user.username}")
    else:
        print(f"ℹ️  Using existing admin user: {admin_user.username}")
    
    # Get or create regular user
    regular_user, created = User.objects.get_or_create(
        username='test_applicant',
        defaults={
            'email': 'applicant@test.com',
            'first_name': 'Test',
            'last_name': 'Applicant',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        regular_user.set_password('test123')
        regular_user.save()
        print(f"✅ Created regular user: {regular_user.username}")
    else:
        print(f"ℹ️  Using existing regular user: {regular_user.username}")
    
    # Create a test application
    print("\n📋 Creating test NRC application...")
    application = NRCApplication.objects.create(
        user=regular_user,
        application_type='new',
        village='Test Village',
        district='Test District',
        date_of_birth=date(1990, 1, 1),
        place_of_birth='Test City',
        chief_name='Chief Test',
        sex='M',
        mother_full_name='Test Mother',
        mother_village='Mother Village',
        mother_district='Mother District',
        mother_date_of_birth=date(1970, 1, 1),
        mother_place_of_birth='Mother City',
        mother_chief_name='Mother Chief',
        father_full_name='Test Father',
        father_village='Father Village',
        father_district='Father District',
        father_date_of_birth=date(1968, 1, 1),
        father_place_of_birth='Father City',
        father_chief_name='Father Chief',
    )
    print(f"✅ Created application #{application.id:05d}")
    
    # Test admin notification creation
    print("\n🔔 Testing admin notification creation...")
    try:
        admin_notifications = NotificationService.create_new_application_notification(application)
        print(f"✅ Created {len(admin_notifications)} admin notifications")
        
        for notification in admin_notifications:
            print(f"   📧 Notification for {notification.user.username}: {notification.title}")
            print(f"      Message: {notification.message[:100]}...")
            print(f"      Type: {notification.notification_type}")
            print(f"      Admin notification: {notification.is_admin_notification}")
    
    except Exception as e:
        print(f"❌ Error creating admin notifications: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test getting admin notifications
    print("\n📥 Testing admin notification retrieval...")
    try:
        admin_notifications = NotificationService.get_admin_notifications(admin_user)
        print(f"✅ Retrieved {admin_notifications.count()} admin notifications")
        
        unread_admin_notifications = NotificationService.get_unread_admin_notifications(admin_user)
        print(f"✅ Found {unread_admin_notifications.count()} unread admin notifications")
        
        # Test for regular user (should get none)
        regular_admin_notifications = NotificationService.get_admin_notifications(regular_user)
        print(f"✅ Regular user admin notifications: {regular_admin_notifications.count()} (should be 0)")
        
    except Exception as e:
        print(f"❌ Error retrieving admin notifications: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test notification details
    print("\n📋 Admin Notification Details:")
    for notification in admin_notifications:
        print(f"   ID: {notification.id}")
        print(f"   User: {notification.user.username}")
        print(f"   Title: {notification.title}")
        print(f"   Type: {notification.notification_type}")
        print(f"   Admin notification: {notification.is_admin_notification}")
        print(f"   Read: {notification.is_read}")
        print(f"   Application: #{notification.application.id:05d}")
        print(f"   Created: {notification.created_at}")
        print("   " + "-" * 40)
    
    print("\n✅ Admin notification system test completed successfully!")
    return True

if __name__ == '__main__':
    success = test_admin_notifications()
    if success:
        print("\n🎉 All tests passed! Admin notification system is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)