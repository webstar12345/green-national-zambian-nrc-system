#!/usr/bin/env python
"""
Test user NRC access and download functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from applications.models import NRCApplication, Notification
from django.test import Client
from django.urls import reverse

User = get_user_model()

def test_user_nrc_access():
    print("🧪 TESTING USER NRC ACCESS")
    print("=" * 50)
    
    # Test user credentials
    username = "mysister@123"
    password = "mysister@123"
    
    try:
        # Get user
        user = User.objects.get(username=username)
        print(f"✅ Found user: {user.username}")
        
        # Get user's approved applications
        approved_apps = NRCApplication.objects.filter(
            user=user, 
            status='approved'
        )
        
        print(f"📋 User has {approved_apps.count()} approved applications")
        
        for app in approved_apps:
            print(f"\n🎫 Application #{app.id:05d}")
            print(f"   NRC Number: {app.nrc_number}")
            print(f"   Status: {app.status}")
            print(f"   Has NRC Images: {'✅' if app.nrc_front_image and app.nrc_back_image else '❌'}")
            
            if app.nrc_front_image and app.nrc_back_image:
                print(f"   📱 Available URLs:")
                print(f"      - Application Detail: /application/{app.id}/")
                print(f"      - View NRC Card: /application/{app.id}/nrc-card/")
                print(f"      - Download Front: /application/{app.id}/download/front/")
                print(f"      - Download Back: /application/{app.id}/download/back/")
                print(f"      - Download Both: /application/{app.id}/download/both/")
                
                # Test client access
                client = Client()
                login_success = client.login(username=username, password=password)
                
                if login_success:
                    print(f"   ✅ Login successful")
                    
                    # Test application detail access
                    detail_url = reverse('applications:application_detail', args=[app.id])
                    response = client.get(detail_url)
                    print(f"   📄 Application Detail: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
                    
                    # Test NRC card view access
                    nrc_url = reverse('applications:view_nrc_card', args=[app.id])
                    response = client.get(nrc_url)
                    print(f"   🎫 NRC Card View: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
                    
                    # Test download access
                    download_front_url = reverse('applications:download_nrc_front', args=[app.id])
                    response = client.get(download_front_url)
                    print(f"   ⬇️  Download Front: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
                    
                    download_back_url = reverse('applications:download_nrc_back', args=[app.id])
                    response = client.get(download_back_url)
                    print(f"   ⬇️  Download Back: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
                    
                    download_both_url = reverse('applications:download_nrc_both', args=[app.id])
                    response = client.get(download_both_url)
                    print(f"   ⬇️  Download Both: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
                    
                else:
                    print(f"   ❌ Login failed")
        
        # Check notifications
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        print(f"\n🔔 User has {notifications.count()} notifications:")
        
        for notif in notifications[:3]:  # Show latest 3
            status = "UNREAD" if not notif.is_read else "READ"
            print(f"   - {notif.notification_type}: {notif.title} ({status})")
            if notif.application:
                print(f"     Related to Application #{notif.application.id:05d}")
        
        print(f"\n" + "=" * 50)
        print("🧪 USER NRC ACCESS TEST COMPLETE")
        
        print(f"\n💡 USER INSTRUCTIONS:")
        print(f"1. Login as: {username}")
        print(f"2. Go to Home page - check for notification alerts")
        print(f"3. Click 'Download Now' button in notifications")
        print(f"4. OR go to 'My Applications' and look for green download buttons")
        print(f"5. OR visit Application Detail page for full download options")
        
    except User.DoesNotExist:
        print(f"❌ User {username} not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_user_nrc_access()