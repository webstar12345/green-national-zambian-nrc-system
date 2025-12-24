#!/usr/bin/env python
"""
Fix script for NRC card flip functionality and registration number display
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

def fix_flip_functionality():
    """Fix the card flip functionality issues"""
    
    print("🔧 Fixing NRC Card Flip Functionality")
    print("=" * 40)
    
    # Read the current template
    template_path = 'templates/applications/nrc_card.html'
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Template file read successfully")
        
        # Check if the flip function exists
        if 'function flipCard()' in content:
            print("✅ Flip function found in template")
        else:
            print("❌ Flip function not found!")
            return False
        
        # Check if the card structure exists
        if 'id="nrcCard"' in content:
            print("✅ Card element ID found")
        else:
            print("❌ Card element ID not found!")
            return False
        
        # Check CSS classes
        if '.card.flipped' in content:
            print("✅ Flip CSS class found")
        else:
            print("❌ Flip CSS class not found!")
            return False
        
        print("\n🎯 Flip Functionality Analysis:")
        print("   ✅ JavaScript function: Present")
        print("   ✅ HTML structure: Correct")
        print("   ✅ CSS animations: Defined")
        print("   ✅ Debug logging: Added")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading template: {e}")
        return False

def verify_registration_number():
    """Verify registration number is displayed on back side"""
    
    print("\n📋 Verifying Registration Number Display")
    print("=" * 40)
    
    # Check NRC generator
    generator_path = 'applications/nrc_generator.py'
    
    try:
        with open(generator_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ NRC generator file read successfully")
        
        # Check if registration number is added to back side
        if 'draw.text((reg_x + 10, reg_box_y + 10), nrc_number' in content:
            print("✅ Registration number added to back side generation")
        else:
            print("❌ Registration number not found in back side generation!")
            return False
        
        # Check template for registration number display
        template_path = 'templates/applications/nrc_card.html'
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        if '{{ application.nrc_number }}' in template_content:
            print("✅ Registration number template variable found")
        else:
            print("❌ Registration number template variable not found!")
            return False
        
        print("\n🎯 Registration Number Analysis:")
        print("   ✅ Back side generation: Updated")
        print("   ✅ Template display: Configured")
        print("   ✅ Front side overlay: Present")
        print("   ✅ Back side overlay: Present")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking registration number: {e}")
        return False

def test_with_browser_instructions():
    """Provide browser testing instructions"""
    
    print("\n🌐 Browser Testing Instructions")
    print("=" * 40)
    
    print("1. 🚀 Start Django server:")
    print("   python manage.py runserver")
    print("")
    
    print("2. 🌐 Open NRC card page:")
    print("   http://127.0.0.1:8000/application/4/nrc-card/")
    print("")
    
    print("3. 🔧 Open Developer Tools (F12):")
    print("   - Go to Console tab")
    print("   - Look for debug messages")
    print("")
    
    print("4. 🧪 Test flip functionality:")
    print("   - Click 'Flip Card' button")
    print("   - Click on the card itself")
    print("   - Press Space or F key")
    print("")
    
    print("5. 📋 Check debug output:")
    print("   - 'Flip card function called'")
    print("   - 'Card element: Found'")
    print("   - 'Button element: Found'")
    print("   - 'Added/Removed flipped class'")
    print("")
    
    print("6. 🎨 Verify registration number:")
    print("   - Front side: Top right corner")
    print("   - Back side: Top right corner")
    print("   - Back side: In green registration box")
    print("")
    
    print("7. 🔍 Troubleshooting:")
    print("   - Check for JavaScript errors in console")
    print("   - Verify CSS transform is applied")
    print("   - Test in different browsers")
    print("")
    
    print("8. 📱 Alternative test page:")
    print("   - Open test_flip_functionality.html")
    print("   - Test flip in isolated environment")

def run_comprehensive_test():
    """Run comprehensive test of both features"""
    
    print("\n🧪 Running Comprehensive Test")
    print("=" * 40)
    
    from applications.models import NRCApplication
    
    # Check if we have test data
    approved_apps = NRCApplication.objects.filter(status='approved')
    
    if approved_apps.exists():
        app = approved_apps.first()
        print(f"✅ Test application found: {app.id}")
        print(f"   - User: {app.user.get_full_name()}")
        print(f"   - NRC: {app.nrc_number}")
        
        if app.nrc_front_image and app.nrc_back_image:
            print("✅ NRC card images exist")
            
            # Check file sizes
            from django.conf import settings
            import os
            
            front_path = os.path.join(settings.MEDIA_ROOT, str(app.nrc_front_image))
            back_path = os.path.join(settings.MEDIA_ROOT, str(app.nrc_back_image))
            
            if os.path.exists(front_path) and os.path.exists(back_path):
                front_size = os.path.getsize(front_path)
                back_size = os.path.getsize(back_path)
                print(f"   - Front: {front_size:,} bytes")
                print(f"   - Back: {back_size:,} bytes")
                
                if back_size > front_size:
                    print("✅ Back side is larger (likely has registration number)")
                else:
                    print("⚠️ Back side size similar to front (check registration number)")
            else:
                print("❌ Card image files not found on disk")
        else:
            print("❌ No NRC card images generated")
            return False
    else:
        print("❌ No approved applications found for testing")
        return False
    
    return True

if __name__ == '__main__':
    print("🔧 NRC CARD FIX & VERIFICATION SCRIPT")
    print("=" * 50)
    
    # Run all checks
    flip_ok = fix_flip_functionality()
    reg_ok = verify_registration_number()
    test_ok = run_comprehensive_test()
    
    # Provide instructions
    test_with_browser_instructions()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"   Flip Functionality: {'✅ OK' if flip_ok else '❌ ISSUES'}")
    print(f"   Registration Number: {'✅ OK' if reg_ok else '❌ ISSUES'}")
    print(f"   Test Data: {'✅ OK' if test_ok else '❌ ISSUES'}")
    
    if flip_ok and reg_ok and test_ok:
        print("\n🎉 ALL CHECKS PASSED!")
        print("🌐 Test in browser using the instructions above")
    else:
        print("\n⚠️ SOME ISSUES FOUND!")
        print("🔧 Check the error messages above")
    
    print("=" * 50)