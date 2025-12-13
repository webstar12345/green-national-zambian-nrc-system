#!/usr/bin/env python
"""
Test Authentic NRC Card Generation
Generate a sample NRC card to verify the new authentic design
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from applications.nrc_generator import generate_nrc_card
from applications.models import NRCApplication
from accounts.models import CustomUser
from datetime import date

def create_test_application():
    """Create a test application for NRC generation"""
    # Create test user if doesn't exist
    try:
        user = CustomUser.objects.get(username='test_nrc_user')
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create_user(
            username='test_nrc_user',
            email='test@example.com',
            first_name='SAKALA',
            last_name='SAMUEL',
            password='testpass123'
        )
    
    # Create test application
    application = NRCApplication(
        user=user,
        date_of_birth=date(1996, 2, 2),
        sex='M',
        village='CHILEKANI',
        district='SINDA',
        chief_name='NYANJE',
        mother_full_name='SAKALA MARY',
        mother_village='CHILEKANI',
        mother_district='SINDA',
        mother_chief_name='NYANJE',
        father_full_name='SAKALA JOHN',
        father_village='CHILEKANI',
        father_district='SINDA',
        father_chief_name='NYANJE',
        status='approved'
    )
    
    return application

def test_nrc_generation():
    """Test the new authentic NRC card generation"""
    print("🆔 Testing Authentic NRC Card Generation")
    print("=" * 50)
    
    # Create test application
    print("📝 Creating test application...")
    application = create_test_application()
    application.id = 999  # Fake ID for testing
    
    try:
        # Generate NRC card
        print("🎨 Generating authentic NRC card...")
        front_path, back_path, nrc_number = generate_nrc_card(application)
        
        print("✅ NRC Card Generated Successfully!")
        print(f"   📄 NRC Number: {nrc_number}")
        print(f"   🖼️  Front Image: {front_path}")
        print(f"   🖼️  Back Image: {back_path}")
        
        # Check if files exist
        import os
        from django.conf import settings
        
        front_full_path = os.path.join(settings.MEDIA_ROOT, front_path)
        back_full_path = os.path.join(settings.MEDIA_ROOT, back_path)
        
        if os.path.exists(front_full_path):
            print(f"   ✅ Front image saved: {front_full_path}")
        else:
            print(f"   ❌ Front image not found: {front_full_path}")
            
        if os.path.exists(back_full_path):
            print(f"   ✅ Back image saved: {back_full_path}")
        else:
            print(f"   ❌ Back image not found: {back_full_path}")
        
        print("\n🎯 New Authentic Features:")
        print("   - Light green background matching real NRC")
        print("   - Proper field layout and positioning")
        print("   - Real NRC number format (Z + 8 digits)")
        print("   - Authentic borders and formatting")
        print("   - Watermark patterns for security")
        print("   - Photo placement like real card")
        print("   - Signature and thumb print areas")
        
        print(f"\n📂 Check the generated images in: {settings.MEDIA_ROOT}/nrc_cards/")
        
    except Exception as e:
        print(f"❌ Error generating NRC card: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_nrc_generation()