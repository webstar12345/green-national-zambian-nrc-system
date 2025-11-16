from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.http import HttpResponse
from datetime import datetime, timedelta
import csv
from .models import NRCApplication
from .forms import NRCApplicationForm, NRCReplacementForm, AdminApplicationForm
from .nrc_generator import generate_nrc_card

@login_required
def home(request):
    user_applications = NRCApplication.objects.filter(user=request.user)[:5]
    context = {
        'user_applications': user_applications,
    }
    return render(request, 'applications/home.html', context)

def about_us(request):
    """About Us page"""
    return render(request, 'applications/about.html')

def services(request):
    """Services page"""
    return render(request, 'applications/services.html')

@login_required
def apply_nrc(request):
    # Check if user already has a new NRC application
    existing_new_application = NRCApplication.objects.filter(
        user=request.user, 
        application_type='new'
    ).exists()
    
    if existing_new_application:
        messages.warning(request, 'You have already submitted a new NRC application. You can only apply once for a new NRC. If you need a replacement, please use the replacement option.')
        return redirect('applications:my_applications')
    
    if request.method == 'POST':
        form = NRCApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.application_type = 'new'  # Force new application type
            application.save()
            messages.success(request, 'Your NRC application has been submitted successfully!')
            return redirect('applications:my_applications')
    else:
        form = NRCApplicationForm()
    
    return render(request, 'applications/apply.html', {'form': form})

@login_required
def apply_replacement(request):
    if request.method == 'POST':
        form = NRCReplacementForm(request.POST, request.FILES)
        if form.is_valid():
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
            messages.success(request, 'Your NRC replacement application has been submitted successfully!')
            return redirect('applications:my_applications')
    else:
        form = NRCReplacementForm()
    
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

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_applications = NRCApplication.objects.count()
    pending_applications = NRCApplication.objects.filter(status='pending').count()
    approved_applications = NRCApplication.objects.filter(status='approved').count()
    rejected_applications = NRCApplication.objects.filter(status='rejected').count()
    
    recent_applications = NRCApplication.objects.all()[:10]
    
    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'recent_applications': recent_applications,
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
        
        # Update application
        old_status = application.status
        application.status = status
        application.admin_notes = admin_notes
        application.save()
        
        # Generate NRC card if status changed to approved and card not yet generated
        if status == 'approved' and not application.nrc_front_image:
            try:
                front_path, back_path, nrc_number = generate_nrc_card(application)
                application.nrc_front_image = front_path
                application.nrc_back_image = back_path
                application.nrc_number = nrc_number
                application.nrc_generated_at = timezone.now()
                application.save()
                messages.success(request, f'Application approved and NRC card generated successfully! NRC Number: {nrc_number}')
            except Exception as e:
                messages.warning(request, f'Application approved but NRC card generation failed: {str(e)}')
        else:
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
    return render(request, 'applications/admin_reports.html')

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
    
    # Export to CSV if requested
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="summary_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Summary Report', f'Generated on {timezone.now().strftime("%Y-%m-%d %H:%M")}'])
        writer.writerow([])
        writer.writerow(['Metric', 'Count'])
        writer.writerow(['Total Applications', total_applications])
        writer.writerow(['New Applications', new_applications])
        writer.writerow(['Replacement Applications', replacement_applications])
        writer.writerow(['Pending', pending_count])
        writer.writerow(['Approved', approved_count])
        writer.writerow(['Rejected', rejected_count])
        writer.writerow(['Male Applicants', male_count])
        writer.writerow(['Female Applicants', female_count])
        writer.writerow(['Recent (30 days)', recent_applications])
        writer.writerow(['Total Users', total_users])
        writer.writerow(['Active Users', active_users])
        
        return response
    
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
    
    # Export to CSV if requested
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="detailed_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Application ID', 'Applicant Name', 'Email', 'Type', 'Status',
            'Village', 'District', 'Sex', 'Date of Birth', 'NRC Number',
            'Date Applied', 'Last Updated'
        ])
        
        for app in applications:
            writer.writerow([
                f"#{app.id:05d}",
                app.user.get_full_name(),
                app.user.email,
                app.get_application_type_display(),
                app.get_status_display(),
                app.village,
                app.district,
                'Male' if app.sex == 'M' else 'Female',
                app.date_of_birth.strftime('%Y-%m-%d'),
                app.nrc_number or 'Not Generated',
                app.created_at.strftime('%Y-%m-%d %H:%M'),
                app.updated_at.strftime('%Y-%m-%d %H:%M'),
            ])
        
        return response
    
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
    
    # Export to CSV if requested
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exception_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Application ID', 'Applicant Name', 'Issue Type', 'Description',
            'Severity', 'Days Pending', 'Status', 'Date Applied'
        ])
        
        for exc in exceptions:
            app = exc['application']
            writer.writerow([
                f"#{app.id:05d}",
                app.user.get_full_name(),
                exc['issue_type'],
                exc['description'],
                exc['severity'],
                exc['days_pending'],
                app.get_status_display(),
                app.created_at.strftime('%Y-%m-%d %H:%M'),
            ])
        
        return response
    
    context = {
        'exceptions': exceptions,
        'total_exceptions': len(exceptions),
    }
    
    return render(request, 'applications/exception_report.html', context)


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
