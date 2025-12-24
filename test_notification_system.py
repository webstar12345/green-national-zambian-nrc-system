#!/usr/bin/env python
"""
Test script for the notification system
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

def test_notification_system():
    print("🔔 Testing Notification System...")
    print("=" * 50)
    
    # Get a test user (create one if needed)
    try:
        user = User.objects.filter(is_staff=False).first()
        if not user:
            print("❌ No regular users found. Please create a user first.")
            return
        
        print(f"✅ Testing with user: {user.username} ({user.email})")
        
        # Get a test application
        application = NRCApplication.objects.filter(user=user).first()
        if not application:
            print("❌ No applications found for this user.")
            return
        
        print(f"✅ Testing with application: #{application.id:05d}")
        
        # Test creating approval notification
        print("\n📝 Creating approval notification...")
        approval_notification = NotificationService.create_approval_notification(application)
        print(f"✅ Created: {approval_notification.title}")
        
        # Test creating NRC ready notification
        print("\n📄 Creating NRC ready notification...")
        nrc_notification = NotificationService.create_nrc_ready_notification(application)
        print(f"✅ Created: {nrc_notification.title}")
        
        # Test getting unread notifications
        print("\n📋 Getting unread notifications...")
        unread = NotificationService.get_unread_notifications(user)
        print(f"✅ Found {unread.count()} unread notifications")
        
        for notification in unread:
            print(f"   - {notification.title}")
        
        # Test marking as read
        if unread.exists():
            print("\n✅ Marking first notification as read...")
            first_notification = unread.first()
            NotificationService.mark_as_read(first_notification.id, user)
            print(f"✅ Marked as read: {first_notification.title}")
        
        # Check unread count again
        unread_after = NotificationService.get_unread_notifications(user)
        print(f"✅ Unread notifications after marking: {unread_after.count()}")
        
        print("\n🎉 Notification system test completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error testing notification system: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_notification_system()