"""
Enhanced Reporting Service for NRC System
Provides comprehensive reporting functionality for admin and officer dashboards
"""

from django.db.models import Count, Q, Avg, Max, Min
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from .models import NRCApplication
import csv
from django.http import HttpResponse

User = get_user_model()


class ReportsService:
    """Service class for generating various reports"""
    
    @staticmethod
    def get_dashboard_stats():
        """Get basic dashboard statistics"""
        total_applications = NRCApplication.objects.count()
        pending_applications = NRCApplication.objects.filter(status='pending').count()
        approved_applications = NRCApplication.objects.filter(status='approved').count()
        rejected_applications = NRCApplication.objects.filter(status='rejected').count()
        
        return {
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'approved_applications': approved_applications,
            'rejected_applications': rejected_applications,
        }
    
    @staticmethod
    def get_summary_report_data(date_from=None, date_to=None):
        """Generate comprehensive summary report data"""
        # Base queryset
        queryset = NRCApplication.objects.all()
        
        # Apply date filters
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        
        # Basic counts
        total_applications = queryset.count()
        pending_count = queryset.filter(status='pending').count()
        approved_count = queryset.filter(status='approved').count()
        rejected_count = queryset.filter(status='rejected').count()
        
        # Application types
        new_applications = queryset.filter(application_type='new').count()
        replacement_applications = queryset.filter(application_type='replacement').count()
        
        # Gender distribution
        male_count = queryset.filter(sex='M').count()
        female_count = queryset.filter(sex='F').count()
        
        # Top districts
        top_districts = (queryset.values('district')
                        .annotate(count=Count('id'))
                        .order_by('-count')[:10])
        
        # Recent activity (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_applications = queryset.filter(created_at__gte=thirty_days_ago).count()
        
        # User statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(last_login__gte=thirty_days_ago).count()
        
        # Processing time analysis
        approved_apps = queryset.filter(status='approved', updated_at__isnull=False)
        avg_processing_time = None
        if approved_apps.exists():
            processing_times = []
            for app in approved_apps:
                if app.updated_at and app.created_at:
                    delta = app.updated_at - app.created_at
                    processing_times.append(delta.days)
            if processing_times:
                avg_processing_time = sum(processing_times) / len(processing_times)
        
        return {
            'total_applications': total_applications,
            'pending_count': pending_count,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
            'new_applications': new_applications,
            'replacement_applications': replacement_applications,
            'male_count': male_count,
            'female_count': female_count,
            'top_districts': top_districts,
            'recent_applications': recent_applications,
            'total_users': total_users,
            'active_users': active_users,
            'avg_processing_time': round(avg_processing_time, 1) if avg_processing_time else None,
            'date_from': date_from,
            'date_to': date_to,
        }
    
    @staticmethod
    def get_detailed_report_data(filters=None):
        """Generate detailed report with filtering"""
        queryset = NRCApplication.objects.select_related('user').all()
        
        if filters:
            if filters.get('status'):
                queryset = queryset.filter(status=filters['status'])
            if filters.get('type'):
                queryset = queryset.filter(application_type=filters['type'])
            if filters.get('date_from'):
                queryset = queryset.filter(created_at__date__gte=filters['date_from'])
            if filters.get('date_to'):
                queryset = queryset.filter(created_at__date__lte=filters['date_to'])
            if filters.get('district'):
                queryset = queryset.filter(district__icontains=filters['district'])
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_exception_report_data():
        """Generate exception report for problematic applications"""
        exceptions = []
        
        # 1. Approved applications without NRC numbers (Critical)
        approved_no_nrc = NRCApplication.objects.filter(
            status='approved',
            nrc_number__isnull=True
        )
        for app in approved_no_nrc:
            exceptions.append({
                'application': app,
                'issue_type': 'Missing NRC Number',
                'severity': 'Critical',
                'description': 'Application approved but no NRC number assigned',
                'days_pending': 0
            })
        
        # 2. Old pending applications (High Priority)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        old_pending = NRCApplication.objects.filter(
            status='pending',
            created_at__lt=thirty_days_ago
        )
        for app in old_pending:
            days_pending = (timezone.now() - app.created_at).days
            exceptions.append({
                'application': app,
                'issue_type': 'Long Pending Application',
                'severity': 'High',
                'description': f'Application pending for {days_pending} days',
                'days_pending': days_pending
            })
        
        # 3. Multiple applications from same user (Medium Priority)
        users_with_multiple = (NRCApplication.objects.values('user')
                              .annotate(count=Count('id'))
                              .filter(count__gt=1))
        
        for user_data in users_with_multiple:
            user_apps = NRCApplication.objects.filter(user_id=user_data['user'])
            latest_app = user_apps.order_by('-created_at').first()
            exceptions.append({
                'application': latest_app,
                'issue_type': 'Multiple Applications',
                'severity': 'Medium',
                'description': f'User has {user_data["count"]} applications',
                'days_pending': 0
            })
        
        # 4. Rejected applications without admin notes (Medium Priority)
        rejected_no_notes = NRCApplication.objects.filter(
            status='rejected',
            Q(admin_notes__isnull=True) | Q(admin_notes='')
        )
        for app in rejected_no_notes:
            exceptions.append({
                'application': app,
                'issue_type': 'Rejected Without Notes',
                'severity': 'Medium',
                'description': 'Application rejected but no admin notes provided',
                'days_pending': 0
            })
        
        # Sort by severity (Critical > High > Medium)
        severity_order = {'Critical': 0, 'High': 1, 'Medium': 2}
        exceptions.sort(key=lambda x: severity_order.get(x['severity'], 3))
        
        return exceptions
    
    @staticmethod
    def get_performance_metrics():
        """Get system performance metrics"""
        now = timezone.now()
        
        # Applications by month (last 12 months)
        monthly_data = []
        for i in range(12):
            month_start = now.replace(day=1) - timedelta(days=30*i)
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end - timedelta(days=month_end.day)
            
            count = NRCApplication.objects.filter(
                created_at__gte=month_start,
                created_at__lte=month_end
            ).count()
            
            monthly_data.append({
                'month': month_start.strftime('%B %Y'),
                'count': count
            })
        
        monthly_data.reverse()
        
        # Processing efficiency
        total_processed = NRCApplication.objects.exclude(status='pending').count()
        total_applications = NRCApplication.objects.count()
        processing_rate = (total_processed / total_applications * 100) if total_applications > 0 else 0
        
        # Average processing time by status
        processing_stats = {}
        for status in ['approved', 'rejected']:
            apps = NRCApplication.objects.filter(status=status, updated_at__isnull=False)
            if apps.exists():
                times = []
                for app in apps:
                    if app.updated_at and app.created_at:
                        delta = app.updated_at - app.created_at
                        times.append(delta.days)
                if times:
                    processing_stats[status] = {
                        'avg_days': round(sum(times) / len(times), 1),
                        'min_days': min(times),
                        'max_days': max(times)
                    }
        
        return {
            'monthly_data': monthly_data,
            'processing_rate': round(processing_rate, 1),
            'processing_stats': processing_stats,
            'total_processed': total_processed,
            'total_applications': total_applications
        }
    
    @staticmethod
    def export_to_csv(data, report_type, response):
        """Export report data to CSV"""
        writer = csv.writer(response)
        
        if report_type == 'summary':
            writer.writerow(['NRC System - Summary Report'])
            writer.writerow([f'Generated on: {timezone.now().strftime("%Y-%m-%d %H:%M")}'])
            writer.writerow([])
            
            writer.writerow(['Metric', 'Count'])
            writer.writerow(['Total Applications', data['total_applications']])
            writer.writerow(['Pending', data['pending_count']])
            writer.writerow(['Approved', data['approved_count']])
            writer.writerow(['Rejected', data['rejected_count']])
            writer.writerow(['New Applications', data['new_applications']])
            writer.writerow(['Replacements', data['replacement_applications']])
            writer.writerow(['Male Applicants', data['male_count']])
            writer.writerow(['Female Applicants', data['female_count']])
            
            writer.writerow([])
            writer.writerow(['Top Districts'])
            writer.writerow(['District', 'Count'])
            for district in data['top_districts']:
                writer.writerow([district['district'], district['count']])
        
        elif report_type == 'detailed':
            writer.writerow(['NRC System - Detailed Report'])
            writer.writerow([f'Generated on: {timezone.now().strftime("%Y-%m-%d %H:%M")}'])
            writer.writerow([])
            
            writer.writerow([
                'ID', 'Name', 'Email', 'Type', 'Status', 'District', 
                'Sex', 'NRC Number', 'Date Applied', 'Date Updated'
            ])
            
            for app in data:
                writer.writerow([
                    f"#{app.id:05d}",
                    app.user.get_full_name(),
                    app.user.email,
                    app.get_application_type_display(),
                    app.get_status_display(),
                    app.district,
                    'Male' if app.sex == 'M' else 'Female',
                    app.nrc_number or 'N/A',
                    app.created_at.strftime('%Y-%m-%d'),
                    app.updated_at.strftime('%Y-%m-%d') if app.updated_at else 'N/A'
                ])
        
        elif report_type == 'exceptions':
            writer.writerow(['NRC System - Exception Report'])
            writer.writerow([f'Generated on: {timezone.now().strftime("%Y-%m-%d %H:%M")}'])
            writer.writerow([])
            
            writer.writerow([
                'Application ID', 'Applicant', 'Issue Type', 'Severity', 
                'Description', 'Days Pending', 'Status', 'Date Applied'
            ])
            
            for exc in data:
                writer.writerow([
                    f"#{exc['application'].id:05d}",
                    exc['application'].user.get_full_name(),
                    exc['issue_type'],
                    exc['severity'],
                    exc['description'],
                    exc['days_pending'],
                    exc['application'].get_status_display(),
                    exc['application'].created_at.strftime('%Y-%m-%d')
                ])
        
        return response
    
    @staticmethod
    def get_export_response(data, report_type, export_format, applications=None, exceptions=None):
        """Get export response in specified format"""
        from .report_exporters import ReportExporter
        
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        
        if export_format == 'pdf':
            if report_type == 'summary':
                filename = f"summary_report_{timestamp}.pdf"
                return ReportExporter.export_summary_to_pdf(data, filename)
            else:
                # For other reports, we'll create a basic PDF
                filename = f"{report_type}_report_{timestamp}.pdf"
                return ReportExporter.export_summary_to_pdf(data, filename)
        
        elif export_format == 'excel':
            if report_type == 'detailed' and applications:
                filename = f"detailed_report_{timestamp}.xlsx"
                return ReportExporter.export_detailed_to_excel(applications, filename)
            elif report_type == 'exceptions' and exceptions:
                filename = f"exceptions_report_{timestamp}.xlsx"
                return ReportExporter.export_exceptions_to_excel(exceptions, filename)
            else:
                # Create a summary Excel file
                filename = f"summary_report_{timestamp}.xlsx"
                return ReportExporter.export_detailed_to_excel([], filename)
        
        elif export_format == 'word':
            filename = f"{report_type}_report_{timestamp}.docx"
            return ReportExporter.export_summary_to_word(data, filename)
        
        else:
            # Default to CSV
            return ReportsService.export_to_csv(data, report_type, response)