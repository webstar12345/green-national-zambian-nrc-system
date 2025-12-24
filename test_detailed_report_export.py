#!/usr/bin/env python
"""
Test Detailed Report Export
Simulate the exact same call that the web view makes
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from applications.models import NRCApplication
from applications.reports_service import ReportsService

def test_detailed_export():
    print("🧪 TESTING DETAILED REPORT EXPORT")
    print("=" * 50)
    
    # Get applications exactly like the view does
    applications = NRCApplication.objects.all()
    
    # Create context data exactly like the view does
    context_data = {
        'total_applications': applications.count(),
        'applications': applications,
    }
    
    print(f"📊 Applications count: {applications.count()}")
    print(f"📋 Context data: {context_data}")
    
    try:
        print(f"\n🚀 Calling ReportsService.get_export_response...")
        print(f"   Parameters:")
        print(f"   - data: {context_data}")
        print(f"   - report_type: 'detailed'")
        print(f"   - export_format: 'pdf'")
        print(f"   - applications: {applications}")
        
        response = ReportsService.get_export_response(
            context_data, 
            'detailed', 
            'pdf', 
            applications=applications
        )
        
        print(f"✅ SUCCESS: Export completed")
        print(f"   Response type: {type(response)}")
        print(f"   Content type: {response.get('Content-Type', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_detailed_export()