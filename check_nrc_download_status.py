#!/usr/bin/env python
"""
Check NRC download status for approved applications
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from applications.models import NRCApplication, Notification
from django.conf import settings

User = get_user_model()

def check_nrc_download_status():
    print("🎫 CHECKING NRC DOWNLOAD STATUS")
    print("=" * 50)
    
    # Get all approved applications
    approved_apps = NRCApplication.objects.filter(status='approved')
    
    print(f"📋 Found {approved_apps.count()} approved applications")
    
    for app in approved_apps:
        print(f"\n👤 User: {app.user.username}")
        print(f"   📄 Application: #{app.id:05d}")
        print(f"   🎫 NRC Number: {app.nrc_number or 'Not generated'}")
        print(f"   📅 Approved: {app.updated_at.strftime('%Y-%m-%d %H:%M')}")
        
        # Check if NRC images exist
        if app.nrc_front_image and app.nrc_back_image:
            print(f"   ✅ NRC Images: Available")
            print(f"      Front: {app.nrc_front_image}")
            print(f"      Back: {app.nrc_back_image}")
            
            # Check if files actually exist on disk
            front_path = os.path.join(settings.MEDIA_ROOT, app.nrc_front_image)
            back_path = os.path.join(settings.MEDIA_ROOT, app.nrc_back_image)
            
            front_exists = os.path.exists(front_path)
            back_exists = os.path.exists(back_path)
            
            print(f"      Front file exists: {'✅' if front_exists else '❌'}")
            print(f"      Back file exists: {'✅' if back_exists else '❌'}")
            
            if front_exists and back_exists:
                print(f"   🎯 READY FOR DOWNLOAD")
                print(f"      Download URLs:")
                print(f"      - Front: /application/{app.id}/download/front/")
                print(f"      - Back: /application/{app.id}/download/back/")
                print(f"      - Both: /application/{app.id}/download/both/")
                print(f"      - View Card: /application/{app.id}/nrc-card/")
            else:
                print(f"   ⚠️  Files missing on disk")
                
        else:
            print(f"   ❌ NRC Images: Not generated")
            print(f"   💡 Admin needs to re-approve to generate NRC card")
        
        # Check notifications
        notifications = Notification.objects.filter(application=app, user=app.user)
        print(f"   🔔 Notifications: {notifications.count()}")
        for notif in notifications:
            status = "UNREAD" if not notif.is_read else "READ"
            print(f"      - {notif.notification_type}: {status}")
    
    print(f"\n" + "=" * 50)
    print("🎫 NRC DOWNLOAD STATUS CHECK COMPLETE")
    
    # Provide user instructions
    print(f"\n💡 HOW TO DOWNLOAD YOUR NRC:")
    print(f"1. Log in as the user (e.g., mysister@123)")
    print(f"2. Go to Home page - look for notification alerts")
    print(f"3. Click 'Download NRC' button in notification")
    print(f"4. OR go to My Applications and click 'View NRC Card'")
    print(f"5. OR visit /application/[ID]/nrc-card/ directly")
    print(f"6. Use download buttons: Front, Back, or Both Sides")

if __name__ == "__main__":
    check_nrc_download_status()