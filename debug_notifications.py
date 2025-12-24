#!/usr/bin/env python
"""
Debug script for notification system
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

def debug_notifications():
    print("🔍 DEBUGGING NOTIFICATION SYSTEM")
    print("=" * 60)
    
    # Check if notifications table exists and has data
    print("\n1. CHECKING NOTIFICATION TABLE:")
    try:
        total_notifications = Notification.objects.count()
        print(f"   ✅ Total notifications in database: {total_notifications}")
        
        if total_notifications > 0:
            print("   📋 Recent notifications:")
            for notification in Notification.objects.all()[:5]:
                print(f"      - {notification.user.username}: {notification.title} ({'READ' if notification.is_read else 'UNREAD'})")
        else:
            print("   ⚠️  No notifications found in database")
    except Exception as e:
        print(f"   ❌ Error accessing notifications: {e}")
    
    # Check applications and their status
    print("\n2. CHECKING APPLICATIONS:")
    try:
        applications = NRCApplication.objects.all()
        print(f"   ✅ Total applications: {applications.count()}")
        
        approved_apps = applications.filter(status='approved')
        print(f"   ✅ Approved applications: {approved_apps.count()}")
        
        if approved_apps.exists():
            print("   📋 Approved applications:")
            for app in approved_apps[:3]:
                print(f"      - App #{app.id:05d} ({app.user.username}) - NRC: {app.nrc_number or 'Not generated'}")
                
                # Check if this app has notifications
                app_notifications = Notification.objects.filter(application=app)
                print(f"        Notifications for this app: {app_notifications.count()}")
                for notif in app_notifications:
                    print(f"          * {notif.title} ({'READ' if notif.is_read else 'UNREAD'})")
        
    except Exception as e:
        print(f"   ❌ Error accessing applications: {e}")
    
    # Check users
    print("\n3. CHECKING USERS:")
    try:
        users = User.objects.all()
        print(f"   ✅ Total users: {users.count()}")
        
        for user in users[:3]:
            user_notifications = Notification.objects.filter(user=user)
            unread_count = user_notifications.filter(is_read=False).count()
            print(f"   👤 {user.username}: {user_notifications.count()} total, {unread_count} unread")
            
    except Exception as e:
        print(f"   ❌ Error accessing users: {e}")
    
    # Test notification creation manually
    print("\n4. TESTING NOTIFICATION CREATION:")
    try:
        # Get a test user and application
        user = User.objects.filter(is_staff=False).first()
        if user:
            application = NRCApplication.objects.filter(user=user).first()
            if application:
                print(f"   🧪 Testing with user: {user.username}, app: #{application.id:05d}")
                
                # Create a test notification
                test_notification = NotificationService.create_approval_notification(application)
                print(f"   ✅ Created test notification: {test_notification.title}")
                print(f"   📧 Notification ID: {test_notification.id}")
                
                # Verify it was saved
                saved_notification = Notification.objects.get(id=test_notification.id)
                print(f"   ✅ Verified notification saved: {saved_notification.title}")
                
            else:
                print("   ⚠️  No applications found for test user")
        else:
            print("   ⚠️  No regular users found for testing")
            
    except Exception as e:
        print(f"   ❌ Error testing notification creation: {e}")
        import traceback
        traceback.print_exc()
    
    # Check admin view integration
    print("\n5. CHECKING ADMIN VIEW INTEGRATION:")
    try:
        from applications.views import admin_application_detail
        print("   ✅ Admin view imported successfully")
        
        # Check if NotificationService is imported in views
        import applications.views as views_module
        import inspect
        
        source = inspect.getsource(views_module.admin_application_detail)
        if 'NotificationService' in source:
            print("   ✅ NotificationService is imported in admin view")
        else:
            print("   ❌ NotificationService NOT found in admin view")
            
        if 'create_approval_notification' in source:
            print("   ✅ create_approval_notification is called in admin view")
        else:
            print("   ❌ create_approval_notification NOT called in admin view")
            
    except Exception as e:
        print(f"   ❌ Error checking admin view: {e}")
    
    print("\n" + "=" * 60)
    print("🔍 DEBUG COMPLETE")
    
    # Provide recommendations
    print("\n💡 RECOMMENDATIONS:")
    if total_notifications == 0:
        print("   1. No notifications found - check if admin approval process is calling NotificationService")
        print("   2. Try approving an application through admin panel")
        print("   3. Check server logs for any errors during approval")
    else:
        print("   1. Notifications are being created")
        print("   2. Check if user is logging in with correct account")
        print("   3. Verify notification display logic in templates")

if __name__ == "__main__":
    debug_notifications()