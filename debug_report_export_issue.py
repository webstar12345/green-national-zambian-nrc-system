#!/usr/bin/env python
"""
Debug Report Export Issue
Identify why the detailed report is still calling export_summary_to_pdf
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from applications.models import NRCApplication
from applications.reports_service import ReportsService

User = get_user_model()

def debug_export_call():
    print("🔍 DEBUGGING REPORT EXPORT ISSUE")
    print("=" * 50)
    
    # Get applications data like the view does
    applications = NRCApplication.objects.all()
    
    context_data = {
        'total_applications': applications.count(),
        'applications': applications,
    }
    
    print(f"📊 Context data keys: {list(context_data.keys())}")
    print(f"📋 Applications count: {applications.count()}")
    print(f"📋 Applications exists: {bool(applications)}")
    
    # Test the logic conditions
    report_type = 'detailed'
    export_format = 'pdf'
    
    print(f"\n🧪 Testing export logic:")
    print(f"   report_type: '{report_type}'")
    print(f"   export_format: '{export_format}'")
    print(f"   applications exists: {bool(applications)}")
    print(f"   report_type == 'detailed': {report_type == 'detailed'}")
    print(f"   applications and report_type == 'detailed': {bool(applications) and report_type == 'detailed'}")
    
    # Check which condition will be met
    if export_format == 'pdf':
        print(f"\n✅ PDF export format detected")
        
        if report_type == 'summary':
            print(f"   → Would call: export_summary_to_pdf")
        elif report_type == 'detailed' and applications:
            print(f"   → Should call: export_detailed_to_pdf")
        elif report_type == 'exceptions':
            print(f"   → Would call: export_exceptions_to_pdf")
        else:
            print(f"   → Would call: export_summary_to_pdf (FALLBACK)")
            print(f"   ❌ This is the problem! Fallback is being triggered")
    
    # Test the actual method call
    try:
        print(f"\n🧪 Testing actual export call...")
        # This should trigger the same logic as the view
        response = ReportsService.get_export_response(
            context_data, 
            'detailed', 
            'pdf', 
            applications=applications
        )
        print(f"✅ Export call succeeded")
        
    except Exception as e:
        print(f"❌ Export call failed: {e}")
        print(f"   This confirms the issue is in the export logic")

def check_method_availability():
    print(f"\n📦 CHECKING METHOD AVAILABILITY")
    print("=" * 50)
    
    try:
        from applications.report_exporters import ReportExporter
        
        methods = [
            'export_summary_to_pdf',
            'export_detailed_to_pdf', 
            'export_exceptions_to_pdf'
        ]
        
        for method in methods:
            if hasattr(ReportExporter, method):
                print(f"✅ {method}: Available")
            else:
                print(f"❌ {method}: Missing")
                
    except Exception as e:
        print(f"❌ Error importing ReportExporter: {e}")

def show_solution():
    print(f"\n💡 SOLUTION")
    print("=" * 50)
    
    print("The issue is likely one of these:")
    print("1. Server cache - Django hasn't reloaded the updated code")
    print("2. Logic condition - The 'applications' parameter isn't being passed correctly")
    print("3. Fallback trigger - Some condition is causing fallback to summary method")
    
    print(f"\n🔧 FIXES TO TRY:")
    print("1. Restart Django server (already done)")
    print("2. Check if applications parameter is properly passed")
    print("3. Add debug prints to reports_service.py")
    print("4. Verify the method exists and is callable")

if __name__ == "__main__":
    debug_export_call()
    check_method_availability()
    show_solution()
    
    print(f"\n" + "=" * 50)
    print("🔍 DEBUG COMPLETE")
    print("=" * 50)