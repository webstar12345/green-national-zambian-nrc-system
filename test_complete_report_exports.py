#!/usr/bin/env python
"""
Test script to verify all report export combinations work correctly
Tests: 3 report types × 4 formats = 12 combinations
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from applications.views import summary_report, detailed_report, exception_report
from applications.models import NRCApplication

User = get_user_model()

def test_all_export_combinations():
    """Test all report export combinations"""
    
    print("🧪 Testing Complete Report Export System")
    print("=" * 50)
    
    # Create a test admin user
    admin_user, created = User.objects.get_or_create(
        email='test_admin@example.com',
        defaults={
            'first_name': 'Test',
            'last_name': 'Admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    factory = RequestFactory()
    
    # Test combinations
    report_types = [
        ('summary', summary_report),
        ('detailed', detailed_report),
        ('exceptions', exception_report)
    ]
    
    export_formats = ['pdf', 'excel', 'word', 'csv']
    
    results = []
    
    for report_name, report_view in report_types:
        print(f"\n📊 Testing {report_name.upper()} Report:")
        print("-" * 30)
        
        for format_type in export_formats:
            try:
                # Create request with export parameter
                request = factory.get(f'/dashboard/reports/{report_name}/', {'export': format_type})
                request.user = admin_user
                
                # Call the view
                response = report_view(request)
                
                # Check response
                if hasattr(response, 'status_code') and response.status_code == 200:
                    content_type = response.get('Content-Type', '')
                    content_disposition = response.get('Content-Disposition', '')
                    
                    # Verify correct content type
                    expected_types = {
                        'pdf': 'application/pdf',
                        'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        'word': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        'csv': 'text/csv'
                    }
                    
                    if expected_types[format_type] in content_type:
                        print(f"  ✅ {format_type.upper()}: SUCCESS")
                        results.append((report_name, format_type, 'SUCCESS'))
                    else:
                        print(f"  ❌ {format_type.upper()}: Wrong content type - {content_type}")
                        results.append((report_name, format_type, f'Wrong content type: {content_type}'))
                else:
                    print(f"  ❌ {format_type.upper()}: HTTP {getattr(response, 'status_code', 'Unknown')}")
                    results.append((report_name, format_type, f'HTTP {getattr(response, "status_code", "Unknown")}'))
                    
            except Exception as e:
                print(f"  ❌ {format_type.upper()}: ERROR - {str(e)}")
                results.append((report_name, format_type, f'ERROR: {str(e)}'))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 EXPORT TEST SUMMARY")
    print("=" * 50)
    
    success_count = sum(1 for _, _, status in results if status == 'SUCCESS')
    total_count = len(results)
    
    print(f"Total Tests: {total_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_count - success_count}")
    print(f"Success Rate: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 ALL EXPORT COMBINATIONS WORKING!")
    else:
        print("\n❌ Some exports failed:")
        for report, format_type, status in results:
            if status != 'SUCCESS':
                print(f"  - {report} {format_type}: {status}")
    
    # Test data availability
    print("\n" + "=" * 50)
    print("📊 DATA AVAILABILITY CHECK")
    print("=" * 50)
    
    total_apps = NRCApplication.objects.count()
    pending_apps = NRCApplication.objects.filter(status='pending').count()
    approved_apps = NRCApplication.objects.filter(status='approved').count()
    
    print(f"Total Applications: {total_apps}")
    print(f"Pending Applications: {pending_apps}")
    print(f"Approved Applications: {approved_apps}")
    
    if total_apps == 0:
        print("⚠️  No applications found - create some test data for better testing")
    else:
        print("✅ Application data available for testing")

if __name__ == '__main__':
    test_all_export_combinations()