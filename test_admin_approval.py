#!/usr/bin/env python
"""
Test admin approval process with notifications
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

def test_admin_approval():
    print("🔧 TESTING ADMIN APPROVAL PROCESS")
    print("=" * 50)
    
    # Find a pending application to test with
    pending_app = NRCApplication.objects.filter(status='pending').first()
    
    if not pending_app:
        print("⚠️  No pending applications found. Creating a test application...")
        
        # Get or create a test user
        test_user, created = User.objects.get_or_create(
            username='test_approval_user',
            defaults={
                'email': 'test@approval.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            print(f"✅ Created test user: {test_user.username}")
        
        # Create a test application
        from datetime import date
        pending_app = NRCApplication.objects.create(
            user=test_user,
            application_type='new',
            status='pending',
            village='Test Village',
            district='Test District',
            date_of_birth=date(1990, 1, 1),
            place_of_birth='Test Place',
            chief_name='Test Chief',
            sex='M',
            mother_full_name='Test Mother',
            mother_village='Test Village',
            mother_district='Test District',
            mother_date_of_birth=date(1970, 1, 1),
            mother_place_of_birth='Test Place',
            mother_chief_name='Test Chief',
            father_full_name='Test Father',
            father_village='Test Village',
            father_district='Test District',
            father_date_of_birth=date(1968, 1, 1),
            father_place_of_birth='Test Place',
            father_chief_name='Test Chief'
        )
        print(f"✅ Created test application: #{pending_app.id:05d}")
    
    print(f"\n🧪 Testing with application #{pending_app.id:05d} ({pending_app.user.username})")
    print(f"   Current status: {pending_app.status}")
    
    # Count notifications before
    notifications_before = Notification.objects.filter(user=pending_app.user).count()
    print(f"   Notifications before: {notifications_before}")
    
    # Simulate admin approval
    print("\n🔄 Simulating admin approval...")
    
    old_status = pending_app.status
    pending_app.status = 'approved'
    pending_app.admin_notes = 'Test approval via script'
    pending_app.save()
    
    print(f"✅ Status changed from {old_status} to {pending_app.status}")
    
    # Create notifications (simulating the admin view logic)
    try:
        print("🔔 Creating approval notification...")
        approval_notif = NotificationService.create_approval_notification(pending_app)
        print(f"✅ Approval notification created: {approval_notif.title}")
        
        # If we want to test NRC generation, we can add it here
        # For now, just create the approval notification
        
    except Exception as e:
        print(f"❌ Error creating notification: {e}")
        import traceback
        traceback.print_exc()
    
    # Count notifications after
    notifications_after = Notification.objects.filter(user=pending_app.user).count()
    print(f"\n📊 Results:")
    print(f"   Notifications before: {notifications_before}")
    print(f"   Notifications after: {notifications_after}")
    print(f"   New notifications: {notifications_after - notifications_before}")
    
    # Show the notifications
    user_notifications = Notification.objects.filter(user=pending_app.user)
    print(f"\n📋 User notifications:")
    for notif in user_notifications:
        status = "UNREAD" if not notif.is_read else "READ"
        print(f"   🔔 {notif.title} ({status})")
        print(f"      {notif.message[:100]}...")
    
    print("\n" + "=" * 50)
    print("🔧 ADMIN APPROVAL TEST COMPLETE")

if __name__ == "__main__":
    test_admin_approval()