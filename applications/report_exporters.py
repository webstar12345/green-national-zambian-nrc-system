"""
Report Export Service for NRC System
Handles professional PDF report generation with enhanced structure and formatting
"""

import io
from datetime import datetime
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings

# PDF Generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart


class ReportExporter:
    """Service class for exporting professional PDF reports"""
    
    # Zambian color scheme
    ZAMBIAN_GREEN = colors.HexColor('#2D5016')
    ZAMBIAN_ORANGE = colors.HexColor('#D97706')
    ZAMBIAN_RED = colors.HexColor('#DC2626')
    HEADER_BG = colors.HexColor('#1F2937')
    TABLE_HEADER = colors.HexColor('#374151')
    TABLE_ROW_ALT = colors.HexColor('#F3F4F6')
    
    @staticmethod
    def _add_header(story, title, subtitle=None):
        """Add professional header to report"""
        styles = getSampleStyleSheet()
        
        # Main title
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=26,
            textColor=ReportExporter.ZAMBIAN_GREEN,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(title, title_style))
        
        # Subtitle if provided
        if subtitle:
            subtitle_style = ParagraphStyle(
                'ReportSubtitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#6B7280'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            story.append(Paragraph(subtitle, subtitle_style))
        
        # Generation timestamp
        timestamp = timezone.now().strftime('%B %d, %Y at %I:%M %p')
        timestamp_style = ParagraphStyle(
            'Timestamp',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#9CA3AF'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        story.append(Paragraph(f"Generated on: {timestamp}", timestamp_style))
        
        # Separator line
        story.append(Spacer(1, 10))
    
    @staticmethod
    def _add_section_header(story, title):
        """Add centered section header"""
        styles = getSampleStyleSheet()
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=ReportExporter.ZAMBIAN_ORANGE,
            spaceAfter=15,
            spaceBefore=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(title, section_style))
    
    @staticmethod
    def _add_subsection_header(story, title, color=None):
        """Add centered subsection header"""
        if not color:
            color = ReportExporter.ZAMBIAN_GREEN
            
        styles = getSampleStyleSheet()
        subsection_style = ParagraphStyle(
            'SubsectionHeader',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=color,
            spaceAfter=10,
            spaceBefore=15,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(title, subsection_style))
    
    @staticmethod
    def _create_styled_table(data, col_widths, header_color=None):
        """Create a professionally styled table"""
        if not header_color:
            header_color = ReportExporter.TABLE_HEADER
        
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        # Build table style
        style_commands = [
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), header_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, header_color),
        ]
        
        # Alternating row colors
        for i in range(1, len(data)):
            if i % 2 == 0:
                style_commands.append(
                    ('BACKGROUND', (0, i), (-1, i), ReportExporter.TABLE_ROW_ALT)
                )
        
        table.setStyle(TableStyle(style_commands))
        return table
    
    @staticmethod
    def export_summary_to_pdf(data, filename="summary_report.pdf"):
        """Export enhanced summary report to PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        story = []
        
        # Header
        ReportExporter._add_header(
            story, 
            "NRC System Summary Report",
            "Comprehensive overview of application statistics and trends"
        )
        
        # Executive Summary Section
        ReportExporter._add_section_header(story, "Executive Summary")
        
        # Key metrics in a grid layout
        key_metrics = [
            ['Metric', 'Value', 'Percentage'],
            ['Total Applications', f"{data['total_applications']:,}", '100%'],
            ['Pending Applications', f"{data['pending_count']:,}", 
             f"{(data['pending_count']/data['total_applications']*100):.1f}%" if data['total_applications'] > 0 else '0%'],
            ['Approved Applications', f"{data['approved_count']:,}", 
             f"{(data['approved_count']/data['total_applications']*100):.1f}%" if data['total_applications'] > 0 else '0%'],
            ['Rejected Applications', f"{data['rejected_count']:,}", 
             f"{(data['rejected_count']/data['total_applications']*100):.1f}%" if data['total_applications'] > 0 else '0%'],
        ]
        
        metrics_table = ReportExporter._create_styled_table(
            key_metrics, 
            [2.5*inch, 1.5*inch, 1.2*inch],
            ReportExporter.ZAMBIAN_GREEN
        )
        story.append(metrics_table)
        story.append(Spacer(1, 20))
        
        # Application Types Section
        ReportExporter._add_section_header(story, "Application Types Breakdown")
        
        type_data = [
            ['Application Type', 'Count', 'Percentage'],
            ['New Applications', f"{data['new_applications']:,}", 
             f"{(data['new_applications']/data['total_applications']*100):.1f}%" if data['total_applications'] > 0 else '0%'],
            ['Replacement Applications', f"{data['replacement_applications']:,}", 
             f"{(data['replacement_applications']/data['total_applications']*100):.1f}%" if data['total_applications'] > 0 else '0%'],
        ]
        
        type_table = ReportExporter._create_styled_table(
            type_data, 
            [2.5*inch, 1.5*inch, 1.2*inch],
            ReportExporter.ZAMBIAN_ORANGE
        )
        story.append(type_table)
        story.append(Spacer(1, 20))
        
        # Demographics Section
        ReportExporter._add_section_header(story, "Demographics Analysis")
        
        demo_data = [
            ['Category', 'Count', 'Percentage'],
            ['Male Applicants', f"{data['male_count']:,}", 
             f"{(data['male_count']/data['total_applications']*100):.1f}%" if data['total_applications'] > 0 else '0%'],
            ['Female Applicants', f"{data['female_count']:,}", 
             f"{(data['female_count']/data['total_applications']*100):.1f}%" if data['total_applications'] > 0 else '0%'],
        ]
        
        demo_table = ReportExporter._create_styled_table(
            demo_data, 
            [2.5*inch, 1.5*inch, 1.2*inch],
            colors.HexColor('#7C3AED')
        )
        story.append(demo_table)
        story.append(Spacer(1, 20))
        
        # Performance Metrics
        if data.get('avg_processing_time'):
            ReportExporter._add_section_header(story, "Performance Metrics")
            
            perf_data = [
                ['Metric', 'Value'],
                ['Average Processing Time', f"{data['avg_processing_time']} days"],
                ['Recent Applications (30 days)', f"{data['recent_applications']:,}"],
                ['Total System Users', f"{data.get('total_users', 0):,}"],
                ['Active Users', f"{data.get('active_users', 0):,}"],
            ]
            
            perf_table = ReportExporter._create_styled_table(
                perf_data, 
                [3*inch, 2*inch],
                colors.HexColor('#059669')
            )
            story.append(perf_table)
            story.append(Spacer(1, 20))
        
        # Geographic Distribution
        if data.get('top_districts'):
            story.append(PageBreak())
            ReportExporter._add_section_header(story, "Geographic Distribution")
            
            districts_data = [['Rank', 'District', 'Applications', 'Percentage', 'Status']]
            
            for i, district in enumerate(data['top_districts'][:15], 1):
                percentage = round((district['count'] / data['total_applications']) * 100, 1) if data['total_applications'] > 0 else 0
                status = "High Volume" if percentage > 10 else "Medium Volume" if percentage > 5 else "Low Volume"
                districts_data.append([
                    str(i),
                    district['district'][:25],  # Truncate long names
                    f"{district['count']:,}",
                    f"{percentage}%",
                    status
                ])
            
            districts_table = ReportExporter._create_styled_table(
                districts_data, 
                [0.5*inch, 2.2*inch, 1*inch, 0.8*inch, 1*inch],
                ReportExporter.ZAMBIAN_RED
            )
            story.append(districts_table)
        
        # Date Range Information
        if data.get('date_from') or data.get('date_to'):
            story.append(Spacer(1, 30))
            ReportExporter._add_section_header(story, "Report Parameters")
            
            date_info = f"Date Range: {data.get('date_from', 'Beginning')} to {data.get('date_to', 'Present')}"
            styles = getSampleStyleSheet()
            story.append(Paragraph(date_info, styles['Normal']))
        
        # Footer
        story.append(Spacer(1, 30))
        styles = getSampleStyleSheet()
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6B7280'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        story.append(Paragraph("This report is confidential and intended for authorized personnel only.", footer_style))
        
        doc.build(story)
        buffer.seek(0)
        
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    @staticmethod
    def export_detailed_to_pdf(applications, filename="detailed_report.pdf"):
        """Export enhanced detailed report to PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=72,
            bottomMargin=72
        )
        story = []
        
        # Convert applications to list for counting
        applications_list = list(applications)
        
        # Header
        ReportExporter._add_header(
            story, 
            "NRC System Detailed Report",
            f"Complete application data and analysis ({len(applications_list)} records)"
        )
        
        # Summary Statistics
        ReportExporter._add_section_header(story, "Report Summary")
        
        total_apps = len(applications_list)
        pending = sum(1 for app in applications_list if app.status == 'pending')
        approved = sum(1 for app in applications_list if app.status == 'approved')
        rejected = sum(1 for app in applications_list if app.status == 'rejected')
        
        summary_data = [
            ['Status', 'Count', 'Percentage'],
            ['Total Applications', f"{total_apps:,}", '100%'],
            ['Pending', f"{pending:,}", f"{(pending/total_apps*100):.1f}%" if total_apps > 0 else '0%'],
            ['Approved', f"{approved:,}", f"{(approved/total_apps*100):.1f}%" if total_apps > 0 else '0%'],
            ['Rejected', f"{rejected:,}", f"{(rejected/total_apps*100):.1f}%" if total_apps > 0 else '0%'],
        ]
        
        summary_table = ReportExporter._create_styled_table(
            summary_data, 
            [2*inch, 1.5*inch, 1.2*inch],
            ReportExporter.ZAMBIAN_GREEN
        )
        story.append(summary_table)
        story.append(Spacer(1, 25))
        
        # Application Details Section
        if applications_list:
            ReportExporter._add_section_header(story, "Application Details")
            
            # Split into chunks for better PDF performance
            chunk_size = 25
            for i in range(0, len(applications_list), chunk_size):
                chunk = applications_list[i:i + chunk_size]
                
                if i > 0:
                    story.append(PageBreak())
                    ReportExporter._add_subsection_header(
                        story, 
                        f"Application Details (continued) - Page {(i//chunk_size) + 1}",
                        ReportExporter.ZAMBIAN_ORANGE
                    )
                
                # Create applications table for this chunk
                app_data = [['ID', 'Applicant', 'Type', 'Status', 'District', 'Date Applied', 'NRC Number']]
                
                for app in chunk:
                    app_data.append([
                        f"#{app.id:05d}",
                        app.user.get_full_name()[:20],  # Truncate long names
                        app.get_application_type_display()[:12],
                        app.get_status_display(),
                        app.district[:15],  # Truncate long district names
                        app.created_at.strftime('%Y-%m-%d'),
                        app.nrc_number[:12] if app.nrc_number else 'Pending'
                    ])
                
                app_table = ReportExporter._create_styled_table(
                    app_data, 
                    [0.7*inch, 1.3*inch, 0.8*inch, 0.8*inch, 1*inch, 0.8*inch, 1*inch],
                    ReportExporter.ZAMBIAN_ORANGE
                )
                
                # Add status-based row coloring
                for row_idx, app in enumerate(chunk, 1):
                    if app.status == 'approved':
                        app_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor('#D1FAE5'))
                        ]))
                    elif app.status == 'rejected':
                        app_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor('#FEE2E2'))
                        ]))
                    elif app.status == 'pending':
                        app_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor('#FEF3C7'))
                        ]))
                
                story.append(app_table)
                story.append(Spacer(1, 15))
            
            # Add legend for status colors
            story.append(Spacer(1, 20))
            ReportExporter._add_section_header(story, "Status Legend")
            
            legend_data = [
                ['Status', 'Color', 'Description'],
                ['Approved', 'Light Green', 'Application has been approved and NRC issued'],
                ['Pending', 'Light Yellow', 'Application is under review'],
                ['Rejected', 'Light Red', 'Application has been rejected'],
            ]
            
            legend_table = ReportExporter._create_styled_table(
                legend_data, 
                [1.5*inch, 1.5*inch, 3*inch],
                colors.HexColor('#4B5563')
            )
            story.append(legend_table)
        
        # Performance note
        if len(applications_list) > 100:
            story.append(Spacer(1, 20))
            styles = getSampleStyleSheet()
            note_style = ParagraphStyle(
                'Note',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#6B7280'),
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique'
            )
            story.append(Paragraph(
                f"Note: This report contains {len(applications_list)} records. "
                "For optimal performance, consider filtering data for smaller datasets.",
                note_style
            ))
        
        # Footer
        story.append(Spacer(1, 30))
        styles = getSampleStyleSheet()
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6B7280'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        story.append(Paragraph("This report contains sensitive personal information. Handle with care.", footer_style))
        
        doc.build(story)
        buffer.seek(0)
        
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    @staticmethod
    def export_exceptions_to_pdf(exceptions, filename="exceptions_report.pdf"):
        """Export enhanced exceptions report to PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        story = []
        
        # Header
        ReportExporter._add_header(
            story, 
            "NRC System Exception Report",
            f"Critical issues and anomalies requiring attention ({len(exceptions)} issues found)"
        )
        
        # Executive Summary
        ReportExporter._add_section_header(story, "Exception Summary")
        
        total_exceptions = len(exceptions)
        critical = sum(1 for exc in exceptions if exc['severity'] == 'Critical')
        high = sum(1 for exc in exceptions if exc['severity'] == 'High')
        medium = sum(1 for exc in exceptions if exc['severity'] == 'Medium')
        
        summary_data = [
            ['Exception Type', 'Count', 'Percentage'],
            ['Total Exceptions', f"{total_exceptions:,}", '100%'],
            ['Critical Issues', f"{critical:,}", f"{(critical/total_exceptions*100):.1f}%" if total_exceptions > 0 else '0%'],
            ['High Priority', f"{high:,}", f"{(high/total_exceptions*100):.1f}%" if total_exceptions > 0 else '0%'],
            ['Medium Priority', f"{medium:,}", f"{(medium/total_exceptions*100):.1f}%" if total_exceptions > 0 else '0%'],
        ]
        
        summary_table = ReportExporter._create_styled_table(
            summary_data, 
            [2.5*inch, 1.5*inch, 1.2*inch],
            ReportExporter.ZAMBIAN_RED
        )
        story.append(summary_table)
        story.append(Spacer(1, 25))
        
        # Priority Actions Section
        if critical > 0 or high > 0:
            ReportExporter._add_section_header(story, "Priority Actions Required")
            
            priority_text = []
            if critical > 0:
                priority_text.append(f"• {critical} CRITICAL issues require immediate attention")
            if high > 0:
                priority_text.append(f"• {high} HIGH priority issues should be resolved within 24 hours")
            if medium > 0:
                priority_text.append(f"• {medium} MEDIUM priority issues should be reviewed this week")
            
            styles = getSampleStyleSheet()
            for text in priority_text:
                story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Exception Details Section
        if exceptions:
            ReportExporter._add_section_header(story, "Exception Details")
            
            # Group exceptions by severity for better organization
            critical_exceptions = [exc for exc in exceptions if exc['severity'] == 'Critical']
            high_exceptions = [exc for exc in exceptions if exc['severity'] == 'High']
            medium_exceptions = [exc for exc in exceptions if exc['severity'] == 'Medium']
            
            # Process each severity level
            for severity, exc_list, color in [
                ('Critical Issues', critical_exceptions, ReportExporter.ZAMBIAN_RED),
                ('High Priority Issues', high_exceptions, ReportExporter.ZAMBIAN_ORANGE),
                ('Medium Priority Issues', medium_exceptions, colors.HexColor('#7C3AED'))
            ]:
                if exc_list:
                    # Add centered subsection header
                    ReportExporter._add_subsection_header(story, severity, color)
                    
                    # Create table for this severity level
                    exc_data = [['ID', 'Applicant', 'Issue Type', 'Description', 'Days Pending']]
                    
                    for exc in exc_list[:20]:  # Limit to 20 per severity for PDF performance
                        exc_data.append([
                            f"#{exc['application'].id:05d}",
                            exc['application'].user.get_full_name()[:18],
                            exc['issue_type'][:15],
                            exc['description'][:40] + ('...' if len(exc['description']) > 40 else ''),
                            str(exc['days_pending'])
                        ])
                    
                    exc_table = ReportExporter._create_styled_table(
                        exc_data, 
                        [0.8*inch, 1.3*inch, 1.2*inch, 2.2*inch, 0.8*inch],
                        color
                    )
                    story.append(exc_table)
                    story.append(Spacer(1, 15))
                    
                    if len(exc_list) > 20:
                        styles = getSampleStyleSheet()
                        note_style = ParagraphStyle(
                            'Note',
                            parent=styles['Normal'],
                            fontSize=9,
                            textColor=colors.HexColor('#6B7280'),
                            alignment=TA_LEFT,
                            fontName='Helvetica-Oblique'
                        )
                        story.append(Paragraph(
                            f"Note: Showing first 20 {severity.lower()} out of {len(exc_list)} total.",
                            note_style
                        ))
                        story.append(Spacer(1, 10))
        
        # Recommendations Section
        story.append(PageBreak())
        ReportExporter._add_section_header(story, "Recommended Actions")
        
        recommendations = [
            "1. Address all CRITICAL issues immediately - these may indicate system integrity problems",
            "2. Review HIGH priority issues within 24 hours to prevent escalation",
            "3. Schedule regular review of MEDIUM priority issues to maintain system health",
            "4. Implement automated monitoring for early detection of similar issues",
            "5. Document resolution steps for future reference and training"
        ]
        
        styles = getSampleStyleSheet()
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
            story.append(Spacer(1, 8))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6B7280'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        story.append(Paragraph("This exception report requires immediate administrative attention.", footer_style))
        
        doc.build(story)
        buffer.seek(0)
        
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response