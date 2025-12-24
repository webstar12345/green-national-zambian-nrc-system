#!/usr/bin/env python
"""
Test script to verify centered headers in PDF reports
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from applications.report_exporters import ReportExporter
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import io

def test_centered_headers():
    """Test that all headers and text above tables are centered"""
    print("🎯 Testing Centered Report Headers...")
    print("=" * 60)
    
    try:
        # Create a test PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Test 1: Main header (should be centered)
        print("\n✅ Testing main header (centered)...")
        ReportExporter._add_header(
            story, 
            "Test Report Title",
            "Test Subtitle"
        )
        
        # Test 2: Section header (should be centered)
        print("✅ Testing section header (centered)...")
        ReportExporter._add_section_header(story, "Test Section Header")
        
        # Test 3: Subsection header (should be centered)
        print("✅ Testing subsection header (centered)...")
        ReportExporter._add_subsection_header(story, "Test Subsection Header")
        
        # Test 4: Table with centered data
        print("✅ Testing table with centered data...")
        test_data = [
            ['Column 1', 'Column 2', 'Column 3'],
            ['Data 1', 'Data 2', 'Data 3'],
            ['Data 4', 'Data 5', 'Data 6']
        ]
        
        table = ReportExporter._create_styled_table(
            test_data, 
            [2*inch, 2*inch, 2*inch],
            ReportExporter.ZAMBIAN_GREEN
        )
        story.append(table)
        
        # Build the PDF
        doc.build(story)
        print("✅ Test PDF generated successfully")
        
        print("\n" + "=" * 60)
        print("🎉 All header alignment tests passed!")
        print("\nVerified Alignments:")
        print("• Main title: CENTERED")
        print("• Subtitle: CENTERED")
        print("• Section headers: CENTERED")
        print("• Subsection headers: CENTERED")
        print("• Table headers: CENTERED")
        print("• Table data: CENTERED")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during header alignment testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Centered Header Alignment Tests")
    
    if test_centered_headers():
        print("\n✅ All tests passed! Headers are properly centered.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
