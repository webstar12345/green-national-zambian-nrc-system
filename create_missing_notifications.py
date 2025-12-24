#!/usr/bin/env python
"""
Create missing notifications for already approved applications
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

def create_missing_notifications():
    print("🔔 CREATING MISSING NOTIFICATIONS")
    print("=" * 50)
    
    # Get all approved applications without notifications
    approved_apps = NRCApplication.objects.filter(status='approved')
    
    print(f"📋 Found {approved_apps.count()} approved applications")
    
    for app in approved_apps:
        print(f"\n🔍 Checking App #{app.id:05d} ({app.user.username})")
        
        # Check if notifications already exist for this app
        existing_notifications = Notification.objects.filter(application=app)
        
        if existing_notifications.exists():
            print(f"   ✅ Already has {existing_notifications.count()} notifications")
            for notif in existing_notifications:
                print(f"      - {notif.title}")
        else:
            print("   ⚠️  No notifications found - creating them now...")
            
            try:
                # Create approval notification
                approval_notif = NotificationService.create_approval_notification(app)
                print(f"   ✅ Created approval notification: {approval_notif.title}")
                
                # If NRC is generated, create NRC ready notification
                if app.nrc_front_image and app.nrc_back_image:
                    nrc_notif = NotificationService.create_nrc_ready_notification(app)
                    print(f"   ✅ Created NRC ready notification: {nrc_notif.title}")
                else:
                    print("   ⚠️  NRC not generated yet - only created approval notification")
                    
            except Exception as e:
                print(f"   ❌ Error creating notifications: {e}")
                import traceback
                traceback.print_exc()
    
    # Show final count
    total_notifications = Notification.objects.count()
    print(f"\n🎉 COMPLETE! Total notifications now: {total_notifications}")
    
    # Show notifications by user
    print("\n👥 NOTIFICATIONS BY USER:")
    for user in User.objects.all():
        user_notifications = Notification.objects.filter(user=user)
        if user_notifications.exists():
            unread_count = user_notifications.filter(is_read=False).count()
            print(f"   👤 {user.username}: {user_notifications.count()} total, {unread_count} unread")
            for notif in user_notifications:
                status = "UNREAD" if not notif.is_read else "READ"
                print(f"      - {notif.title} ({status})")

if __name__ == "__main__":
    create_missing_notifications()