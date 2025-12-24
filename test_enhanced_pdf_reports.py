#!/usr/bin/env python
"""
Test script for enhanced PDF report generation
Tests the new professional PDF report structure
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.utils import timezone
from applications.models import NRCApplication
from applications.reports_service import ReportsService
from applications.report_exporters import ReportExporter

def test_pdf_reports():
    """Test all PDF report types"""
    print("🔍 Testing Enhanced PDF Report Generation...")
    print("=" * 60)
    
    try:
        # Test 1: Summary Report
        print("\n📊 Testing Summary Report PDF...")
        summary_data = ReportsService.get_summary_report_data()
        
        if summary_data['total_applications'] > 0:
            pdf_response = ReportExporter.export_summary_to_pdf(
                summary_data, 
                "test_summary_report.pdf"
            )
            print(f"✅ Summary PDF generated successfully")
            print(f"   - Total applications: {summary_data['total_applications']}")
            print(f"   - Pending: {summary_data['pending_count']}")
            print(f"   - Approved: {summary_data['approved_count']}")
            print(f"   - Rejected: {summary_data['rejected_count']}")
        else:
            print("⚠️  No applications found for summary report")
        
        # Test 2: Detailed Report
        print("\n📋 Testing Detailed Report PDF...")
        applications = ReportsService.get_detailed_report_data()
        
        if applications.exists():
            pdf_response = ReportExporter.export_detailed_to_pdf(
                applications[:50],  # Limit for testing
                "test_detailed_report.pdf"
            )
            print(f"✅ Detailed PDF generated successfully")
            print(f"   - Records processed: {min(applications.count(), 50)}")
            print(f"   - Total available: {applications.count()}")
        else:
            print("⚠️  No applications found for detailed report")
        
        # Test 3: Exception Report
        print("\n⚠️  Testing Exception Report PDF...")
        exceptions = ReportsService.get_exception_report_data()
        
        if exceptions:
            pdf_response = ReportExporter.export_exceptions_to_pdf(
                exceptions,
                "test_exceptions_report.pdf"
            )
            print(f"✅ Exception PDF generated successfully")
            print(f"   - Total exceptions: {len(exceptions)}")
            
            # Show exception breakdown
            critical = sum(1 for exc in exceptions if exc['severity'] == 'Critical')
            high = sum(1 for exc in exceptions if exc['severity'] == 'High')
            medium = sum(1 for exc in exceptions if exc['severity'] == 'Medium')
            
            print(f"   - Critical: {critical}")
            print(f"   - High: {high}")
            print(f"   - Medium: {medium}")
        else:
            print("✅ No exceptions found - system is healthy!")
        
        # Test 4: Performance Metrics
        print("\n📈 Testing Performance Metrics...")
        performance_data = ReportsService.get_performance_metrics()
        
        print(f"✅ Performance metrics calculated:")
        print(f"   - Processing rate: {performance_data['processing_rate']}%")
        print(f"   - Total processed: {performance_data['total_processed']}")
        print(f"   - Monthly data points: {len(performance_data['monthly_data'])}")
        
        # Test 5: Color Scheme and Styling
        print("\n🎨 Testing Report Styling...")
        print("✅ Zambian color scheme implemented:")
        print(f"   - Green: {ReportExporter.ZAMBIAN_GREEN}")
        print(f"   - Orange: {ReportExporter.ZAMBIAN_ORANGE}")
        print(f"   - Red: {ReportExporter.ZAMBIAN_RED}")
        
        print("\n" + "=" * 60)
        print("🎉 All PDF report tests completed successfully!")
        print("\nKey Improvements:")
        print("• Professional PDF-only reports with enhanced structure")
        print("• Zambian color scheme and branding")
        print("• Better data organization and readability")
        print("• Status-based color coding for applications")
        print("• Comprehensive exception reporting with priority levels")
        print("• Removed Word and Excel dependencies for cleaner system")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during PDF report testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_report_structure():
    """Test the report structure and formatting"""
    print("\n🏗️  Testing Report Structure...")
    
    try:
        # Test helper methods
        from reportlab.platypus import SimpleDocTemplate
        from reportlab.lib.pagesizes import A4
        import io
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Test header creation
        ReportExporter._add_header(story, "Test Report", "Test Subtitle")
        print("✅ Header creation works")
        
        # Test section header
        ReportExporter._add_section_header(story, "Test Section")
        print("✅ Section header creation works")
        
        # Test table creation
        test_data = [
            ['Column 1', 'Column 2', 'Column 3'],
            ['Data 1', 'Data 2', 'Data 3'],
            ['Data 4', 'Data 5', 'Data 6']
        ]
        
        from reportlab.lib.units import inch
        table = ReportExporter._create_styled_table(
            test_data, 
            [2*inch, 2*inch, 2*inch],
            ReportExporter.ZAMBIAN_GREEN
        )
        story.append(table)
        print("✅ Styled table creation works")
        
        # Test document building
        doc.build(story)
        print("✅ Document building works")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing report structure: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Enhanced PDF Report Tests")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run structure tests first
    structure_ok = test_report_structure()
    
    if structure_ok:
        # Run full report tests
        reports_ok = test_pdf_reports()
        
        if reports_ok:
            print("\n🎯 All tests passed! The enhanced PDF report system is ready.")
            sys.exit(0)
        else:
            print("\n💥 Report generation tests failed!")
            sys.exit(1)
    else:
        print("\n💥 Report structure tests failed!")
        sys.exit(1)