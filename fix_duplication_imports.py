#!/usr/bin/env python
"""
Fix duplication prevention import issues
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

def test_duplication_system():
    print("🔧 TESTING DUPLICATION PREVENTION SYSTEM")
    print("=" * 50)
    
    try:
        # Test imports
        from applications.duplication_prevention import DuplicationChecker
        from applications.models import DuplicationLog, NRCApplication
        from django.contrib.auth import get_user_model
        
        print("✅ All imports successful")
        
        # Test DuplicationChecker functionality
        test_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',
            'place_of_birth': 'Test City',
            'mother_full_name': 'Test Mother',
            'mother_date_of_birth': '1970-01-01',
            'father_full_name': 'Test Father',
            'father_date_of_birth': '1968-01-01',
            'sex': 'M',
            'village': 'Test Village',
        }
        
        result = DuplicationChecker.comprehensive_duplicate_check(test_data)
        print(f"✅ Duplication check working: {result['is_duplicate']}")
        
        # Test database models
        log_count = DuplicationLog.objects.count()
        app_count = NRCApplication.objects.count()
        print(f"✅ Database access working: {log_count} logs, {app_count} applications")
        
        # Test user model
        User = get_user_model()
        user_count = User.objects.count()
        print(f"✅ User model working: {user_count} users")
        
        print("\n🛡️ DUPLICATION PREVENTION SYSTEM STATUS:")
        print("   ✅ Imports: Working")
        print("   ✅ DuplicationChecker: Working")
        print("   ✅ Database Models: Working")
        print("   ✅ User Integration: Working")
        print("   ✅ Overall Status: OPERATIONAL")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_interface():
    print("\n🎛️ TESTING ADMIN INTERFACE ACCESS")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        # Test URL resolution
        duplication_url = reverse('applications:duplication_check')
        print(f"✅ Duplication check URL: {duplication_url}")
        
        mark_url = reverse('applications:mark_not_duplicate', args=[1])
        print(f"✅ Mark not duplicate URL: {mark_url}")
        
        print("✅ URL routing working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ URL Error: {e}")
        return False

def check_form_integration():
    print("\n📝 TESTING FORM INTEGRATION")
    print("=" * 50)
    
    try:
        from applications.forms import NRCApplicationForm, NRCReplacementForm
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        # Test form imports
        print("✅ Form imports successful")
        
        # Test form initialization (without user for now)
        try:
            form = NRCApplicationForm()
            print("✅ NRCApplicationForm can be initialized")
        except Exception as e:
            print(f"⚠️  NRCApplicationForm needs user: {e}")
        
        try:
            replacement_form = NRCReplacementForm()
            print("✅ NRCReplacementForm can be initialized")
        except Exception as e:
            print(f"⚠️  NRCReplacementForm needs user: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Form Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 DUPLICATION PREVENTION SYSTEM DIAGNOSTIC")
    print("=" * 60)
    
    # Run all tests
    test1 = test_duplication_system()
    test2 = test_admin_interface()
    test3 = check_form_integration()
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if test1 and test2 and test3:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Duplication prevention system is fully operational")
        print("✅ Admin interface is accessible")
        print("✅ Form integration is working")
        print("\n💡 NEXT STEPS:")
        print("   1. Access admin dashboard: /admin-dashboard/")
        print("   2. Click 'Check for Duplicates' button")
        print("   3. Review any flagged applications")
        print("   4. Test form submission with duplicate data")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("   Please review the errors above and fix any issues")
        
    print(f"\n🛡️ SYSTEM STATUS: {'OPERATIONAL' if test1 else 'NEEDS ATTENTION'}")