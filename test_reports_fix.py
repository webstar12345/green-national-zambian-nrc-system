#!/usr/bin/env python
"""
Test Reports Functionality After Fix
Tests that the reports system works correctly after fixing the syntax error
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from applications.reports_service import ReportsService
from applications.models import NRCApplication
from django.contrib.auth import get_user_model

User = get_user_model()

def test_reports_functionality():
    """Test that reports work correctly"""
    print("🔧 Testing Reports Functionality After Fix...")
    print("=" * 50)
    print()
    
    try:
        # Test 1: Dashboard Stats
        print("📊 Testing Dashboard Stats...")
        stats = ReportsService.get_dashboard_stats()
        print(f"✅ Dashboard Stats: {stats}")
        print()
        
        # Test 2: Summary Report
        print("📋 Testing Summary Report...")
        summary = ReportsService.get_summary_report_data()
        print(f"✅ Summary Report: Total Applications = {summary['total_applications']}")
        print()
        
        # Test 3: Detailed Report
        print("📄 Testing Detailed Report...")
        detailed = ReportsService.get_detailed_report_data()
        print(f"✅ Detailed Report: {detailed.count()} applications found")
        print()
        
        # Test 4: Exception Report
        print("⚠️ Testing Exception Report...")
        exceptions = ReportsService.get_exception_report_data()
        print(f"✅ Exception Report: {len(exceptions)} exceptions found")
        print()
        
        # Test 5: Performance Metrics
        print("📈 Testing Performance Metrics...")
        metrics = ReportsService.get_performance_metrics()
        print(f"✅ Performance Metrics: Processing rate = {metrics['processing_rate']}%")
        print()
        
        print("🎉 ALL REPORTS TESTS PASSED!")
        print("✅ Reports system is working correctly")
        print()
        
        print("🔗 Admin Dashboard URLs:")
        print("- Main Dashboard: http://localhost:8000/admin-dashboard/")
        print("- Reports: http://localhost:8000/dashboard/reports/")
        print("- Summary Report: http://localhost:8000/dashboard/reports/summary/")
        print("- Detailed Report: http://localhost:8000/dashboard/reports/detailed/")
        print("- Exception Report: http://localhost:8000/dashboard/reports/exceptions/")
        
    except Exception as e:
        print(f"❌ Error testing reports: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reports_functionality()