#!/usr/bin/env python
"""
Test notification display functionality
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

def test_notification_display():
    print("📱 TESTING NOTIFICATION DISPLAY")
    print("=" * 50)
    
    # Test for each user with notifications
    users_with_notifications = User.objects.filter(notifications__isnull=False).distinct()
    
    print(f"👥 Found {users_with_notifications.count()} users with notifications")
    
    for user in users_with_notifications:
        print(f"\n👤 Testing for user: {user.username}")
        
        # Test unread notifications (what home page shows)
        unread_notifications = NotificationService.get_unread_notifications(user)
        print(f"   📬 Unread notifications: {unread_notifications.count()}")
        
        for notification in unread_notifications:
            print(f"      🔔 {notification.title}")
            print(f"         Type: {notification.notification_type}")
            print(f"         Message: {notification.message[:100]}...")
            if notification.application:
                print(f"         Application: #{notification.application.id:05d}")
                print(f"         NRC Number: {notification.application.nrc_number or 'Not generated'}")
        
        # Test notification count endpoint
        print(f"   📊 Notification count: {unread_notifications.count()}")
        
        # Test all notifications (what notifications page shows)
        all_notifications = user.notifications.all()
        print(f"   📋 Total notifications: {all_notifications.count()}")
    
    print("\n🧪 TESTING NOTIFICATION ACTIONS:")
    
    # Test marking as read
    first_notification = Notification.objects.filter(is_read=False).first()
    if first_notification:
        print(f"   📝 Testing mark as read for: {first_notification.title}")
        success = NotificationService.mark_as_read(first_notification.id, first_notification.user)
        print(f"   ✅ Mark as read result: {success}")
        
        # Verify it was marked as read
        first_notification.refresh_from_db()
        print(f"   ✅ Notification is now: {'READ' if first_notification.is_read else 'UNREAD'}")
    
    print("\n🎯 TESTING SPECIFIC USER SCENARIOS:")
    
    # Test specific users mentioned in debug
    test_users = ['mysister@123', 'teddy@123']
    
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            print(f"\n👤 {username}:")
            
            unread = NotificationService.get_unread_notifications(user)
            print(f"   📬 Unread: {unread.count()}")
            
            for notif in unread:
                print(f"      🔔 {notif.title}")
                if notif.application and notif.notification_type == 'nrc_ready':
                    print(f"         🎫 Can download NRC: {bool(notif.application.nrc_front_image)}")
                    
        except User.DoesNotExist:
            print(f"   ❌ User {username} not found")
    
    print("\n" + "=" * 50)
    print("📱 NOTIFICATION DISPLAY TEST COMPLETE")

if __name__ == "__main__":
    test_notification_display()