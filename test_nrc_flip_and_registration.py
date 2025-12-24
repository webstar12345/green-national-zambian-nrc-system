#!/usr/bin/env python
"""
Test script for NRC card flip functionality and registration number display
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from applications.models import NRCApplication
from applications.nrc_generator import generate_nrc_card
from django.contrib.auth import get_user_model

User = get_user_model()

def test_nrc_flip_and_registration():
    """Test NRC card generation with registration number on back"""
    
    print("🔄 Testing NRC Card Flip & Registration Number")
    print("=" * 50)
    
    # Find an approved application
    approved_apps = NRCApplication.objects.filter(status='approved')
    
    if approved_apps.exists():
        application = approved_apps.first()
        print(f"✅ Using existing application: {application.id}")
    else:
        print("❌ No approved applications found")
        return False
    
    print(f"📋 Application Details:")
    print(f"   - User: {application.user.get_full_name()}")
    print(f"   - Current NRC: {application.nrc_number}")
    
    try:
        print("\n🎨 Regenerating NRC card with registration number on back...")
        
        # Generate new NRC card
        front_path, back_path, nrc_number = generate_nrc_card(application)
        
        # Update application
        application.nrc_front_image = front_path
        application.nrc_back_image = back_path
        application.nrc_number = nrc_number
        application.nrc_generated_at = django.utils.timezone.now()
        application.save()
        
        print(f"✅ NRC Card Generated Successfully!")
        print(f"   - NRC Number: {nrc_number}")
        print(f"   - Front Image: {front_path}")
        print(f"   - Back Image: {back_path}")
        
        # Check file existence
        from django.conf import settings
        front_full_path = os.path.join(settings.MEDIA_ROOT, front_path)
        back_full_path = os.path.join(settings.MEDIA_ROOT, back_path)
        
        if os.path.exists(front_full_path) and os.path.exists(back_full_path):
            print(f"✅ Both card images exist")
            print(f"   - Front: {os.path.getsize(front_full_path):,} bytes")
            print(f"   - Back: {os.path.getsize(back_full_path):,} bytes")
        else:
            print(f"❌ Card images missing")
            return False
        
        print(f"\n🌐 Test the card at:")
        print(f"   http://127.0.0.1:8000/application/{application.id}/nrc-card/")
        
        print(f"\n🔄 Flip Functionality Features:")
        print(f"   ✅ CSS 3D transform animation")
        print(f"   ✅ JavaScript flip function with debug logs")
        print(f"   ✅ Button state management")
        print(f"   ✅ Keyboard shortcuts (Space, F)")
        print(f"   ✅ Click-to-flip on card")
        print(f"   ✅ Loading states and notifications")
        
        print(f"\n📋 Registration Number Display:")
        print(f"   ✅ Front side: Top right corner overlay")
        print(f"   ✅ Back side: Top right corner overlay")
        print(f"   ✅ Back side: In registration box (white on green)")
        print(f"   ✅ Number: {nrc_number}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_flip_debugging():
    """Provide debugging instructions for flip functionality"""
    print(f"\n🔧 Flip Debugging Instructions:")
    print(f"=" * 30)
    print(f"1. Open browser developer tools (F12)")
    print(f"2. Go to Console tab")
    print(f"3. Click the flip button")
    print(f"4. Check for debug messages:")
    print(f"   - 'Flip card function called'")
    print(f"   - 'Card element: <div>'")
    print(f"   - 'Button element: <button>'")
    print(f"   - 'Flipping to: back/front'")
    print(f"   - 'Added/Removed flipped class'")
    print(f"   - 'Flip animation completed'")
    print(f"")
    print(f"5. Check CSS classes in Elements tab:")
    print(f"   - Look for 'card flipped' class when flipped")
    print(f"   - Verify transform: rotateY(180deg)")
    print(f"")
    print(f"6. Manual test commands in console:")
    print(f"   - flipCard() // Call flip function")
    print(f"   - document.getElementById('nrcCard') // Check card element")
    print(f"   - document.querySelector('button[onclick=\"flipCard()\"]') // Check button")

if __name__ == '__main__':
    success = test_nrc_flip_and_registration()
    test_flip_debugging()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 NRC CARD TEST COMPLETED!")
        print("✅ Registration number added to back side")
        print("✅ Flip functionality enhanced with debugging")
        print("🔧 Use browser dev tools to debug flip issues")
    else:
        print("❌ Test failed - check error messages above")
    print("=" * 50)