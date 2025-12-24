from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.http import HttpResponse, FileResponse, Http404, JsonResponse
from datetime import datetime, timedelta
import csv
import os
import zipfile
from django.conf import settings
from .models import NRCApplication
from .forms import NRCApplicationForm, NRCReplacementForm, AdminApplicationForm
from .nrc_generator import generate_nrc_card
import base64
from django.core.files.base import ContentFile
from io import BytesIO

def home(request):
    """Public landing page - no login required"""
    user_applications = None
    unread_notifications = None
    
    if request.user.is_authenticated:
        user_applications = NRCApplication.objects.filter(user=request.user)[:5]
        
        # Get unread notifications for the user
        from .notifications import NotificationService
        unread_notifications = NotificationService.get_unread_notifications(request.user)
    
    context = {
        'user_applications': user_applications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'applications/home.html', context)

def landing(request):
    """Enhanced landing page showcasing all features"""
    return render(request, 'applications/landing.html')

def about_us(request):
    """About Us page"""
    return render(request, 'applications/about.html')

def services(request):
    """Services page"""
    return render(request, 'applications/services.html')

@login_required
def apply_nrc(request):
    # Double-check authentication (redundant but safe)
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to apply for an NRC.')
        return redirect('accounts:login')
    
    # Check if user already has a new NRC application
    existing_new_application = NRCApplication.objects.filter(
        user=request.user, 
        application_type='new'
    ).exists()
    
    if existing_new_application:
        messages.warning(request, 'You have already submitted a new NRC application. You can only apply once for a new NRC. If you need a replacement, please use the replacement option.')
        return redirect('applications:my_applications')
    
    if request.method == 'POST':
        form = NRCApplicationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.user = request.user
                application.application_type = 'new'  # Force new application type
                application.save()
                
                # Create admin notifications for new application
                from .notifications import NotificationService
                try:
                    admin_notifications = NotificationService.create_new_application_notification(application)
                    print(f"✅ Created {len(admin_notifications)} admin notifications for new application #{application.id:05d}")
                except Exception as e:
                    print(f"❌ Error creating admin notifications: {e}")
                    # Don't fail the application submission if notification fails
                
                messages.success(request, 'Your NRC application has been submitted successfully!')
                return redirect('applications:my_applications')
            except Exception as e:
                messages.error(request, f'Error submitting application: {str(e)}')
    else:
        form = NRCApplicationForm(user=request.user)
    
    return render(request, 'applications/apply.html', {'form': form})

@login_required
def apply_replacement(request):
    # Double-check authentication (redundant but safe)
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to apply for an NRC replacement.')
        return redirect('accounts:login')
        
    if request.method == 'POST':
        form = NRCReplacementForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.user = request.user
                application.application_type = 'replacement'
                
                # Copy user's existing information from their profile or first application
                first_app = NRCApplication.objects.filter(user=request.user, application_type='new').first()
                if first_app:
                    # Copy information from first application
                    application.village = first_app.village
                    application.district = first_app.district
                    application.date_of_birth = first_app.date_of_birth
                    application.place_of_birth = first_app.place_of_birth
                    application.chief_name = first_app.chief_name
                    application.sex = first_app.sex
                    application.photo = first_app.photo
                    application.mother_full_name = first_app.mother_full_name
                    application.mother_village = first_app.mother_village
                    application.mother_district = first_app.mother_district
                    application.mother_date_of_birth = first_app.mother_date_of_birth
                    application.mother_place_of_birth = first_app.mother_place_of_birth
                    application.mother_chief_name = first_app.mother_chief_name
                    application.father_full_name = first_app.father_full_name
                    application.father_village = first_app.father_village
                    application.father_district = first_app.father_district
                    application.father_date_of_birth = first_app.father_date_of_birth
                    application.father_place_of_birth = first_app.father_place_of_birth
                    application.father_chief_name = first_app.father_chief_name
                
                application.save()
                
                # Create admin notifications for replacement application
                from .notifications import NotificationService
                try:
                    admin_notifications = NotificationService.create_new_application_notification(application)
                    print(f"✅ Created {len(admin_notifications)} admin notifications for replacement application #{application.id:05d}")
                except Exception as e:
                    print(f"❌ Error creating admin notifications: {e}")
                    # Don't fail the application submission if notification fails
                
                messages.success(request, 'Your NRC replacement application has been submitted successfully!')
                return redirect('applications:my_applications')
            except Exception as e:
                messages.error(request, f'Error submitting replacement application: {str(e)}')
    else:
        form = NRCReplacementForm(user=request.user)
    
    # Check if user has an approved new application
    has_approved_nrc = NRCApplication.objects.filter(
        user=request.user,
        application_type='new',
        status='approved'
    ).exists()
    
    return render(request, 'applications/apply_replacement.html', {
        'form': form,
        'has_approved_nrc': has_approved_nrc
    })

@login_required
def my_applications(request):
    applications = NRCApplication.objects.filter(user=request.user)
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'applications/my_applications.html', {'page_obj': page_obj})

@login_required
def application_detail(request, pk):
    application = get_object_or_404(NRCApplication, pk=pk, user=request.user)
    return render(request, 'applications/application_detail.html', {'application': application})

@login_required
def view_nrc_card(request, pk):
    application = get_object_or_404(NRCApplication, pk=pk, user=request.user)
    
    # Only show NRC card if application is approved
    if application.status != 'approved' or not application.nrc_front_image:
        messages.error(request, 'NRC card is not available yet. Your application must be approved first.')
        return redirect('applications:application_detail', pk=pk)
    
    return render(request, 'applications/nrc_card.html', {'application': application})

@login_required
def signature_pad(request, pk):
    """Digital signature pad for touchscreen devices"""
    application = get_object_or_404(NRCApplication, pk=pk, user=request.user)
    
    # Only allow signature if application is approved
    if application.status != 'approved':
        messages.error(request, 'You can only add a signature after your application is approved.')
        return redirect('applications:application_detail', pk=pk)
    
    if request.method == 'POST':
        signature_data = request.POST.get('signature_data')
        
        if signature_data:
            try:
                # Remove data URL prefix if present
                if signature_data.startswith('data:image/png;base64,'):
                    signature_data = signature_data.replace('data:image/png;base64,', '')
                
                # Save signature to application
                application.digital_signature = signature_data
                application.save()
                
                # Regenerate NRC card with new signature
                front_path, back_path, nrc_number = generate_nrc_card(application)
                application.nrc_front_image = front_path
                application.nrc_back_image = back_path
                application.nrc_number = nrc_number
                application.nrc_generated_at = timezone.now()
                application.save()
                
                messages.success(request, 'Your digital signature has been saved and your NRC card has been updated!')
                return redirect('applications:view_nrc_card', pk=pk)
                
            except Exception as e:
                messages.error(request, f'Error saving signature: {str(e)}')
        else:
            messages.error(request, 'Please provide a signature before saving.')
    
    return render(request, 'applications/signature_pad.html', {'application': application})

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_applications = NRCApplication.objects.count()
    pending_applications = NRCApplication.objects.filter(status='pending').count()
    approved_applications = NRCApplication.objects.filter(status='approved').count()
    rejected_applications = NRCApplication.objects.filter(status='rejected').count()
    
    recent_applications = NRCApplication.objects.all()[:10]
    
    # Get admin notifications
    from .notifications import NotificationService
    admin_notifications = NotificationService.get_admin_notifications(request.user, limit=5)
    unread_admin_notifications = NotificationService.get_unread_admin_notifications(request.user)
    
    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'recent_applications': recent_applications,
        'admin_notifications': admin_notifications,
        'unread_admin_notifications_count': unread_admin_notifications.count(),
    }
    return render(request, 'applications/admin_dashboard.html', context)

@user_passes_test(is_admin)
def admin_applications(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    applications = NRCApplication.objects.all()
    
    if search_query:
        applications = applications.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'applications/admin_applications.html', context)

@user_passes_test(is_admin)
def admin_application_detail(request, pk):
    application = get_object_or_404(NRCApplication, pk=pk)
    
    if request.method == 'POST':
        # Get form data directly from POST
        status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '')
        
        # Store old status to check for changes
        old_status = application.status
        
        # Perform duplication check before approval
        if status == 'approved' and old_status != 'approved':
            from .duplication_prevention import DuplicationChecker, log_duplication_attempt
            
            # Prepare application data for duplication check
            application_data = {
                'first_name': application.user.first_name,
                'last_name': application.user.last_name,
                'date_of_birth': application.date_of_birth,
                'place_of_birth': application.place_of_birth,
                'mother_full_name': application.mother_full_name,
                'mother_date_of_birth': application.mother_date_of_birth,
                'father_full_name': application.father_full_name,
                'father_date_of_birth': application.father_date_of_birth,
                'sex': application.sex,
                'village': application.village,
            }
            
            # Check for duplicates
            duplicate_check = DuplicationChecker.comprehensive_duplicate_check(
                application_data, application.user, application.id
            )
            
            if duplicate_check['is_duplicate']:
                # Log the duplication attempt
                log_duplication_attempt(
                    duplicate_check, 
                    application.user, 
                    request, 
                    request.user, 
                    'warned',
                    f"Admin {request.user.username} was warned about potential duplicate but may proceed with approval."
                )
                
                # Show warning to admin but allow override
                duplicate_warnings = []
                if duplicate_check['duplicate_type'] == 'exact_match':
                    matching_apps = duplicate_check['matching_applications']
                    app_ids = [f"#{app.id:05d}" for app in matching_apps]
                    duplicate_warnings.append(
                        f"⚠️ EXACT DUPLICATE DETECTED: Identical applications found ({', '.join(app_ids)}). "
                        "Please verify this is not a duplicate person before approving."
                    )
                elif duplicate_check['duplicate_type'] == 'similar_match':
                    matching_apps = duplicate_check['matching_applications']
                    scores = duplicate_check['similarity_scores']
                    app_details = []
                    for app, score in zip(matching_apps, scores):
                        app_details.append(f"#{app.id:05d} ({score:.1%} similar)")
                    duplicate_warnings.append(
                        f"⚠️ SIMILAR APPLICATIONS DETECTED: {', '.join(app_details)}. "
                        "Please verify this is not a duplicate person before approving."
                    )
                
                # Add warnings to messages
                for warning in duplicate_warnings:
                    messages.warning(request, warning)
                
                # Don't auto-approve, let admin review
                messages.info(request, "Application status updated. Please review duplication warnings above before final approval.")
        
        # Update application
        application.status = status
        application.admin_notes = admin_notes
        application.save()
        
        # Import notification service
        from .notifications import NotificationService
        
        # Create notifications based on status change
        if old_status != status:
            print(f"🔄 Status changed from {old_status} to {status}")  # Debug log
            
            if status == 'approved':
                try:
                    # Generate NRC card if not yet generated
                    if not application.nrc_front_image:
                        print("🎫 Generating NRC card...")  # Debug log
                        try:
                            front_path, back_path, nrc_number = generate_nrc_card(application)
                            application.nrc_front_image = front_path
                            application.nrc_back_image = back_path
                            application.nrc_number = nrc_number
                            application.nrc_generated_at = timezone.now()
                            application.save()
                            print(f"✅ NRC card generated: {nrc_number}")  # Debug log
                            
                            # Create approval notification
                            print("🔔 Creating approval notification...")  # Debug log
                            approval_notif = NotificationService.create_approval_notification(application)
                            print(f"✅ Approval notification created: {approval_notif.id}")  # Debug log
                            
                            # Also create NRC ready notification
                            print("🔔 Creating NRC ready notification...")  # Debug log
                            nrc_notif = NotificationService.create_nrc_ready_notification(application)
                            print(f"✅ NRC ready notification created: {nrc_notif.id}")  # Debug log
                            
                            messages.success(request, f'Application approved and NRC card generated successfully! NRC Number: {nrc_number}. User has been notified.')
                        except Exception as e:
                            print(f"❌ NRC generation failed: {e}")  # Debug log
                            # Still create approval notification even if card generation fails
                            approval_notif = NotificationService.create_approval_notification(application)
                            print(f"✅ Approval notification created (fallback): {approval_notif.id}")  # Debug log
                            messages.warning(request, f'Application approved but NRC card generation failed: {str(e)}. User has been notified of approval.')
                    else:
                        print("🎫 NRC already exists, creating approval notification...")  # Debug log
                        # NRC already exists, just create approval notification
                        approval_notif = NotificationService.create_approval_notification(application)
                        print(f"✅ Approval notification created: {approval_notif.id}")  # Debug log
                        messages.success(request, 'Application approved successfully! User has been notified.')
                        
                except Exception as e:
                    print(f"❌ Error in approval process: {e}")  # Debug log
                    import traceback
                    traceback.print_exc()
                    messages.error(request, f'Error during approval process: {str(e)}')
                    
            elif status == 'rejected':
                try:
                    print("🔔 Creating rejection notification...")  # Debug log
                    # Create rejection notification
                    rejection_notif = NotificationService.create_rejection_notification(application, admin_notes)
                    print(f"✅ Rejection notification created: {rejection_notif.id}")  # Debug log
                    messages.success(request, 'Application rejected successfully! User has been notified.')
                except Exception as e:
                    print(f"❌ Error creating rejection notification: {e}")  # Debug log
                    messages.error(request, f'Application rejected but notification failed: {str(e)}')
        else:
            print("ℹ️  Status unchanged, no notifications created")  # Debug log
            messages.success(request, 'Application updated successfully!')
        
        return redirect('applications:admin_application_detail', pk=pk)
    
    return render(request, 'applications/admin_application_detail.html', {
        'application': application,
    })

@user_passes_test(is_admin)
def admin_users(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    search_query = request.GET.get('search', '')
    
    users = User.objects.all()
    
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'applications/admin_users.html', context)

@user_passes_test(is_admin)
def admin_user_detail(request, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = get_object_or_404(User, pk=user_id)
    user_applications = NRCApplication.objects.filter(user=user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'toggle_staff':
            user.is_staff = not user.is_staff
            user.save()
            messages.success(request, f'User staff status updated to: {"Staff" if user.is_staff else "Regular User"}')
        elif action == 'toggle_active':
            user.is_active = not user.is_active
            user.save()
            messages.success(request, f'User account {"activated" if user.is_active else "deactivated"}')
        
        return redirect('applications:admin_user_detail', user_id=user_id)
    
    context = {
        'viewed_user': user,
        'user_applications': user_applications,
    }
    return render(request, 'applications/admin_user_detail.html', context)

# Report Views
@user_passes_test(is_admin)
def admin_reports(request):
    """Main reports page with options"""
    from .reports_service import ReportsService
    
    # Get basic stats for the reports overview
    stats = ReportsService.get_dashboard_stats()
    
    # Get recent exceptions count
    exceptions = ReportsService.get_exception_report_data()
    critical_exceptions = len([e for e in exceptions if e['severity'] == 'Critical'])
    high_exceptions = len([e for e in exceptions if e['severity'] == 'High'])
    
    context = {
        **stats,
        'total_exceptions': len(exceptions),
        'critical_exceptions': critical_exceptions,
        'high_exceptions': high_exceptions,
    }
    
    return render(request, 'applications/admin_reports.html', context)

@user_passes_test(is_admin)
def summary_report(request):
    """Generate summary report with statistics and trends"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Date range filter
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    applications = NRCApplication.objects.all()
    
    if date_from:
        applications = applications.filter(created_at__gte=date_from)
    if date_to:
        applications = applications.filter(created_at__lte=date_to)
    
    # Statistics
    total_applications = applications.count()
    new_applications = applications.filter(application_type='new').count()
    replacement_applications = applications.filter(application_type='replacement').count()
    
    pending_count = applications.filter(status='pending').count()
    approved_count = applications.filter(status='approved').count()
    rejected_count = applications.filter(status='rejected').count()
    
    # Gender statistics
    male_count = applications.filter(sex='M').count()
    female_count = applications.filter(sex='F').count()
    
    # Recent trends (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_applications = applications.filter(created_at__gte=thirty_days_ago).count()
    
    # Applications by district (top 10)
    top_districts = applications.values('district').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Total users
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    context = {
        'total_applications': total_applications,
        'new_applications': new_applications,
        'replacement_applications': replacement_applications,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'male_count': male_count,
        'female_count': female_count,
        'recent_applications': recent_applications,
        'top_districts': top_districts,
        'total_users': total_users,
        'active_users': active_users,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    # Handle export requests
    export_format = request.GET.get('export')
    if export_format in ['csv', 'pdf']:
        from .reports_service import ReportsService
        
        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="summary_report.csv"'
            return ReportsService.export_to_csv(context, 'summary', response)
        else:
            return ReportsService.get_export_response(context, 'summary', export_format)
    
    return render(request, 'applications/summary_report.html', context)

@user_passes_test(is_admin)
def detailed_report(request):
    """Generate detailed report with all application data"""
    # Filters
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    district_filter = request.GET.get('district', '')
    
    applications = NRCApplication.objects.all().select_related('user')
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    if type_filter:
        applications = applications.filter(application_type=type_filter)
    if date_from:
        applications = applications.filter(created_at__gte=date_from)
    if date_to:
        applications = applications.filter(created_at__lte=date_to)
    if district_filter:
        applications = applications.filter(district__icontains=district_filter)
    
    # Get unique districts for filter
    districts = NRCApplication.objects.values_list('district', flat=True).distinct().order_by('district')
    
    # Handle export requests
    export_format = request.GET.get('export')
    if export_format in ['csv', 'pdf']:
        from .reports_service import ReportsService
        
        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="detailed_report.csv"'
            return ReportsService.export_to_csv(applications, 'detailed', response)
        else:
            # For PDF export, we need the full data context
            context_data = {
                'total_applications': applications.count(),
                'applications': applications,
            }
            return ReportsService.get_export_response(context_data, 'detailed', export_format, applications=applications)
    
    # Pagination
    paginator = Paginator(applications, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'date_from': date_from,
        'date_to': date_to,
        'district_filter': district_filter,
        'districts': districts,
    }
    
    return render(request, 'applications/detailed_report.html', context)

@user_passes_test(is_admin)
def exception_report(request):
    """Generate exception report for applications with issues"""
    
    # Find applications with potential issues
    exceptions = []
    
    # 1. Pending applications older than 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    old_pending = NRCApplication.objects.filter(
        status='pending',
        created_at__lt=thirty_days_ago
    ).select_related('user')
    
    for app in old_pending:
        exceptions.append({
            'application': app,
            'issue_type': 'Old Pending Application',
            'description': f'Application has been pending for more than 30 days',
            'severity': 'High',
            'days_pending': (timezone.now() - app.created_at).days
        })
    
    # 2. Approved applications without NRC number
    approved_no_nrc = NRCApplication.objects.filter(
        status='approved',
        nrc_number__isnull=True
    ).select_related('user')
    
    for app in approved_no_nrc:
        exceptions.append({
            'application': app,
            'issue_type': 'Missing NRC Number',
            'description': 'Application approved but NRC card not generated',
            'severity': 'Critical',
            'days_pending': (timezone.now() - app.updated_at).days
        })
    
    # 3. Multiple applications from same user
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    users_with_multiple = NRCApplication.objects.values('user').annotate(
        count=Count('id')
    ).filter(count__gt=2)
    
    for item in users_with_multiple:
        user = User.objects.get(id=item['user'])
        apps = NRCApplication.objects.filter(user=user)
        exceptions.append({
            'application': apps.first(),
            'issue_type': 'Multiple Applications',
            'description': f'User has {item["count"]} applications',
            'severity': 'Medium',
            'days_pending': 0
        })
    
    # 4. Rejected applications with no admin notes
    rejected_no_notes = NRCApplication.objects.filter(
        status='rejected',
        admin_notes=''
    ).select_related('user')
    
    for app in rejected_no_notes:
        exceptions.append({
            'application': app,
            'issue_type': 'Missing Rejection Reason',
            'description': 'Application rejected without admin notes',
            'severity': 'Medium',
            'days_pending': (timezone.now() - app.updated_at).days
        })
    
    # Handle export requests
    export_format = request.GET.get('export')
    if export_format in ['csv', 'pdf']:
        from .reports_service import ReportsService
        
        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exception_report.csv"'
            return ReportsService.export_to_csv(exceptions, 'exceptions', response)
        else:
            context_data = {
                'exceptions': exceptions,
                'total_exceptions': len(exceptions),
            }
            return ReportsService.get_export_response(context_data, 'exceptions', export_format, exceptions=exceptions)
    
    context = {
        'exceptions': exceptions,
        'total_exceptions': len(exceptions),
    }
    
    return render(request, 'applications/exception_report.html', context)


# Officer Dashboard and Reports
@login_required
def officer_dashboard(request):
    """Officer dashboard with limited reporting capabilities"""
    from .reports_service import ReportsService
    
    # Basic stats
    stats = ReportsService.get_dashboard_stats()
    
    # Officer-specific metrics
    recent_applications = NRCApplication.objects.order_by('-created_at')[:10]
    
    # Performance metrics
    performance = ReportsService.get_performance_metrics()
    
    context = {
        **stats,
        'recent_applications': recent_applications,
        'monthly_data': performance['monthly_data'][:6],  # Last 6 months
        'processing_rate': performance['processing_rate'],
    }
    
    return render(request, 'applications/officer_dashboard.html', context)


@login_required
def officer_summary_report(request):
    """Officer summary report with basic statistics"""
    from .reports_service import ReportsService
    
    # Date filters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Convert string dates to date objects
    if date_from:
        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
    if date_to:
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
    
    # Get report data (limited for officers)
    context = ReportsService.get_summary_report_data(date_from, date_to)
    
    # Remove sensitive data for officers
    context['is_officer_view'] = True
    
    # Export to CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="officer_summary_report.csv"'
        return ReportsService.export_to_csv(context, 'summary', response)
    
    return render(request, 'applications/officer_summary_report.html', context)


@login_required
def officer_applications_report(request):
    """Officer applications report with basic filtering"""
    from .reports_service import ReportsService
    
    # Filters (limited for officers)
    filters = {
        'status': request.GET.get('status', ''),
        'type': request.GET.get('type', ''),
        'date_from': request.GET.get('date_from'),
        'date_to': request.GET.get('date_to'),
    }
    
    # Remove empty filters
    filters = {k: v for k, v in filters.items() if v}
    
    # Get filtered applications
    applications = ReportsService.get_detailed_report_data(filters)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(applications, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': request.GET.get('status', ''),
        'type_filter': request.GET.get('type', ''),
        'date_from': request.GET.get('date_from', ''),
        'date_to': request.GET.get('date_to', ''),
        'is_officer_view': True,
    }
    
    # Export to CSV (limited data for officers)
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="officer_applications_report.csv"'
        return ReportsService.export_to_csv(applications, 'detailed', response)
    
    return render(request, 'applications/officer_applications_report.html', context)


# AI Assistant Views
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .ai_assistant import NRCAssistant
import json

@login_required
@require_http_methods(["POST"])
def chat_message(request):
    """Handle chat messages from users"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        language = data.get('language', 'en')
        
        if not message:
            return JsonResponse({
                'success': False,
                'error': 'Message is required'
            }, status=400)
        
        # Get or create assistant for this session
        session_key = f'assistant_{language}'
        if session_key not in request.session:
            assistant = NRCAssistant(language=language)
            request.session[session_key] = True
        else:
            assistant = NRCAssistant(language=language)
        
        # Send message and get response
        response = assistant.send_message(message)
        
        return JsonResponse(response)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@require_http_methods(["GET"])
def get_quick_responses(request):
    """Get quick response suggestions"""
    language = request.GET.get('language', 'en')
    assistant = NRCAssistant(language=language)
    
    return JsonResponse({
        'success': True,
        'quick_responses': assistant.get_quick_responses(),
        'language': language
    })


@login_required
def ai_demo(request):
    """AI Assistant demo page"""
    return render(request, 'applications/ai_demo.html')

# NRC Card Download Views
@login_required
def download_nrc_front(request, pk):
    """Download NRC front side"""
    application = get_object_or_404(NRCApplication, pk=pk, user=request.user)
    
    if application.status != 'approved' or not application.nrc_front_image:
        messages.error(request, 'NRC card is not available for download.')
        return redirect('applications:application_detail', pk=pk)
    
    try:
        # Get the full file path
        file_path = os.path.join(settings.MEDIA_ROOT, application.nrc_front_image)
        
        if os.path.exists(file_path):
            # Create response with proper filename
            filename = f"NRC_Front_{application.nrc_number}.png"
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=filename,
                content_type='image/png'
            )
            return response
        else:
            messages.error(request, 'NRC front image file not found.')
            return redirect('applications:view_nrc_card', pk=pk)
            
    except Exception as e:
        messages.error(request, f'Error downloading NRC front: {str(e)}')
        return redirect('applications:view_nrc_card', pk=pk)

@login_required
def download_nrc_back(request, pk):
    """Download NRC back side"""
    application = get_object_or_404(NRCApplication, pk=pk, user=request.user)
    
    if application.status != 'approved' or not application.nrc_back_image:
        messages.error(request, 'NRC card is not available for download.')
        return redirect('applications:application_detail', pk=pk)
    
    try:
        # Get the full file path
        file_path = os.path.join(settings.MEDIA_ROOT, application.nrc_back_image)
        
        if os.path.exists(file_path):
            # Create response with proper filename
            filename = f"NRC_Back_{application.nrc_number}.png"
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=filename,
                content_type='image/png'
            )
            return response
        else:
            messages.error(request, 'NRC back image file not found.')
            return redirect('applications:view_nrc_card', pk=pk)
            
    except Exception as e:
        messages.error(request, f'Error downloading NRC back: {str(e)}')
        return redirect('applications:view_nrc_card', pk=pk)

@login_required
def download_nrc_both(request, pk):
    """Download both NRC sides as a ZIP file"""
    application = get_object_or_404(NRCApplication, pk=pk, user=request.user)
    
    if application.status != 'approved' or not application.nrc_front_image or not application.nrc_back_image:
        messages.error(request, 'NRC card is not available for download.')
        return redirect('applications:application_detail', pk=pk)
    
    try:
        # Get file paths
        front_path = os.path.join(settings.MEDIA_ROOT, application.nrc_front_image)
        back_path = os.path.join(settings.MEDIA_ROOT, application.nrc_back_image)
        
        if not os.path.exists(front_path) or not os.path.exists(back_path):
            messages.error(request, 'One or both NRC image files not found.')
            return redirect('applications:view_nrc_card', pk=pk)
        
        # Create ZIP file in memory
        from io import BytesIO
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add front image
            zip_file.write(front_path, f"NRC_Front_{application.nrc_number}.png")
            # Add back image
            zip_file.write(back_path, f"NRC_Back_{application.nrc_number}.png")
        
        zip_buffer.seek(0)
        
        # Create response
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="NRC_Complete_{application.nrc_number}.zip"'
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error creating ZIP file: {str(e)}')
        return redirect('applications:view_nrc_card', pk=pk)

# Admin Download Views (for admin users to download any NRC)
@user_passes_test(is_admin)
def admin_download_nrc_front(request, pk):
    """Admin download NRC front side"""
    application = get_object_or_404(NRCApplication, pk=pk)
    
    if application.status != 'approved' or not application.nrc_front_image:
        messages.error(request, 'NRC card is not available for download.')
        return redirect('applications:admin_application_detail', pk=pk)
    
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, application.nrc_front_image)
        
        if os.path.exists(file_path):
            filename = f"NRC_Front_{application.nrc_number}_{application.user.get_full_name().replace(' ', '_')}.png"
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=filename,
                content_type='image/png'
            )
            return response
        else:
            messages.error(request, 'NRC front image file not found.')
            return redirect('applications:admin_application_detail', pk=pk)
            
    except Exception as e:
        messages.error(request, f'Error downloading NRC front: {str(e)}')
        return redirect('applications:admin_application_detail', pk=pk)

@user_passes_test(is_admin)
def admin_download_nrc_back(request, pk):
    """Admin download NRC back side"""
    application = get_object_or_404(NRCApplication, pk=pk)
    
    if application.status != 'approved' or not application.nrc_back_image:
        messages.error(request, 'NRC card is not available for download.')
        return redirect('applications:admin_application_detail', pk=pk)
    
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, application.nrc_back_image)
        
        if os.path.exists(file_path):
            filename = f"NRC_Back_{application.nrc_number}_{application.user.get_full_name().replace(' ', '_')}.png"
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=filename,
                content_type='image/png'
            )
            return response
        else:
            messages.error(request, 'NRC back image file not found.')
            return redirect('applications:admin_application_detail', pk=pk)
            
    except Exception as e:
        messages.error(request, f'Error downloading NRC back: {str(e)}')
        return redirect('applications:admin_application_detail', pk=pk)

@user_passes_test(is_admin)
def admin_download_nrc_both(request, pk):
    """Admin download both NRC sides as ZIP"""
    application = get_object_or_404(NRCApplication, pk=pk)
    
    if application.status != 'approved' or not application.nrc_front_image or not application.nrc_back_image:
        messages.error(request, 'NRC card is not available for download.')
        return redirect('applications:admin_application_detail', pk=pk)
    
    try:
        front_path = os.path.join(settings.MEDIA_ROOT, application.nrc_front_image)
        back_path = os.path.join(settings.MEDIA_ROOT, application.nrc_back_image)
        
        if not os.path.exists(front_path) or not os.path.exists(back_path):
            messages.error(request, 'One or both NRC image files not found.')
            return redirect('applications:admin_application_detail', pk=pk)
        
        from io import BytesIO
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(front_path, f"NRC_Front_{application.nrc_number}.png")
            zip_file.write(back_path, f"NRC_Back_{application.nrc_number}.png")
        
        zip_buffer.seek(0)
        
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="NRC_Complete_{application.nrc_number}_{application.user.get_full_name().replace(" ", "_")}.zip"'
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error creating ZIP file: {str(e)}')
        return redirect('applications:admin_application_detail', pk=pk)

# Notification Views
@login_required
def notifications(request):
    """View all notifications for the user"""
    from .notifications import NotificationService
    
    all_notifications = request.user.notifications.all()
    unread_count = NotificationService.get_unread_notifications(request.user).count()
    
    # Pagination
    paginator = Paginator(all_notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'unread_count': unread_count,
    }
    return render(request, 'applications/notifications.html', context)

@login_required
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    from .notifications import NotificationService
    
    if NotificationService.mark_as_read(notification_id, request.user):
        messages.success(request, 'Notification marked as read.')
    else:
        messages.error(request, 'Notification not found.')
    
    return redirect('applications:notifications')

@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    from .notifications import NotificationService
    
    NotificationService.mark_all_as_read(request.user)
    messages.success(request, 'All notifications marked as read.')
    
    return redirect('applications:notifications')

@login_required
def get_notification_count(request):
    """AJAX endpoint to get unread notification count"""
    from .notifications import NotificationService
    
    unread_count = NotificationService.get_unread_notifications(request.user).count()
    
    return JsonResponse({
        'unread_count': unread_count
    })

@user_passes_test(is_admin)
def duplication_check(request):
    """
    Admin view to check for potential duplicates and manage duplication prevention
    """
    from .duplication_prevention import DuplicationChecker
    from .models import DuplicationLog
    from django.db.models import Q
    import json
    
    # Get all applications for duplicate checking
    all_applications = NRCApplication.objects.filter(
        Q(status='pending') | Q(status='approved')
    ).order_by('-created_at')
    
    potential_duplicates = []
    exact_duplicates = 0
    similar_matches = 0
    clean_applications = 0
    
    # Check each application for duplicates
    for app in all_applications:
        application_data = {
            'first_name': app.user.first_name,
            'last_name': app.user.last_name,
            'date_of_birth': app.date_of_birth,
            'place_of_birth': app.place_of_birth,
            'mother_full_name': app.mother_full_name,
            'mother_date_of_birth': app.mother_date_of_birth,
            'father_full_name': app.father_full_name,
            'father_date_of_birth': app.father_date_of_birth,
            'sex': app.sex,
            'village': app.village,
        }
        
        # Check for duplicates
        duplicate_check = DuplicationChecker.comprehensive_duplicate_check(
            application_data, app.user, app.id
        )
        
        if duplicate_check['is_duplicate']:
            duplicate_info = {
                'application': app,
                'duplicate_type': duplicate_check['duplicate_type'],
                'matching_applications': duplicate_check['matching_applications'],
                'similarity_scores': [score * 100 for score in duplicate_check['similarity_scores']],  # Convert to percentage
            }
            potential_duplicates.append(duplicate_info)
            
            if duplicate_check['duplicate_type'] == 'exact_match':
                exact_duplicates += 1
            elif duplicate_check['duplicate_type'] == 'similar_match':
                similar_matches += 1
        else:
            clean_applications += 1
    
    # Get recent duplication logs
    duplication_logs = DuplicationLog.objects.all()[:20]
    
    # Count blocked attempts
    blocked_attempts = DuplicationLog.objects.filter(action_taken='blocked').count()
    
    context = {
        'potential_duplicates': potential_duplicates,
        'exact_duplicates': exact_duplicates,
        'similar_matches': similar_matches,
        'clean_applications': clean_applications,
        'blocked_attempts': blocked_attempts,
        'duplication_logs': duplication_logs,
    }
    
    return render(request, 'applications/duplication_check.html', context)

@user_passes_test(is_admin)
def mark_not_duplicate(request, application_id):
    """
    Mark an application as not a duplicate (admin override)
    """
    if request.method == 'POST':
        try:
            application = get_object_or_404(NRCApplication, id=application_id)
            
            # Log the admin override
            from .models import DuplicationLog
            DuplicationLog.objects.create(
                detection_type='similar_match',  # Assume it was similar match
                action_taken='approved_override',
                attempted_application_data={
                    'application_id': application.id,
                    'user': application.user.username,
                },
                matching_application_ids=[],
                similarity_scores=[],
                user=application.user,
                admin_user=request.user,
                admin_notes=f"Admin {request.user.username} marked application #{application.id:05d} as not a duplicate.",
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})