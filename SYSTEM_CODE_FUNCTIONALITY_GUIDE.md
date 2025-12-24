# ZAMBIAN NRC SYSTEM - CODE FUNCTIONALITY GUIDE

## 📋 OVERVIEW
This document provides comprehensive code functionality explanations for the Zambian National Registration Card (NRC) System. It covers user authentication, registration, logout, NRC applications, and replacement processes.

---

## 🔐 AUTHENTICATION SYSTEM

### 1. USER REGISTRATION (SIGNUP)

**File:** `accounts/views.py` - `SignUpView` class
**URL:** `/accounts/signup/`
**Template:** `templates/accounts/signup.html`

```python
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:otp_verify')

    def form_valid(self, form):
        # Save user but don't log them in yet
        response = super().form_valid(form)
        user = self.object
        
        # Generate and send OTP for email verification
        otp_code = user.generate_otp()
        
        # Store user info in session for OTP verification
        self.request.session['pending_signup_user_id'] = user.id
        self.request.session['pending_signup_email'] = user.email
        
        # Send OTP email or show fallback
        email_success = OTPService.send_otp_email(user.email, otp_code, user.get_full_name())
        
        return response
```

**Functionality:**
- Creates new user account with email, name, phone number
- Generates 6-digit OTP code for email verification
- Stores user session data for verification step
- Sends OTP via email (Gmail SMTP)
- Redirects to OTP verification page
- **Admin Bypass:** New signups are always regular users (not admins)

**Form Fields:** `accounts/forms.py` - `CustomUserCreationForm`
```python
fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')
```

---

### 2. USER LOGIN

**File:** `accounts/views.py` - `CustomLoginView` class
**URL:** `/accounts/login/`
**Template:** `templates/accounts/login.html`

```python
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            # ADMIN BYPASS - Skip OTP for admin users
            if user.is_staff or user.is_superuser:
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(self.request, f'Welcome back, {user.get_full_name()}! (Admin Access)')
                return redirect('applications:home')
            
            # Regular users go through OTP verification
            otp_code = user.generate_otp()
            self.request.session['pending_login_user_id'] = user.id
            
            # Send OTP email with Gmail SMTP
            email_success = OTPService.send_otp_email(user.email, otp_code, user.get_full_name())
            
            return redirect('accounts:otp_verify')
```

**Key Features:**
- **Admin Bypass:** Staff/superuser accounts skip OTP verification
- **OTP Security:** Regular users must verify 6-digit code sent to email
- **Session Management:** Stores pending login data in session
- **Gmail Integration:** Uses Gmail SMTP for reliable email delivery
- **Fallback System:** Shows OTP in browser if email fails (development mode)

---

### 3. OTP VERIFICATION

**File:** `accounts/views.py` - `otp_verify` function
**URL:** `/accounts/otp-verify/`
**Template:** `templates/accounts/otp_verify.html`

```python
def otp_verify(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        
        # Check for pending login or signup verification
        pending_login_user_id = request.session.get('pending_login_user_id')
        pending_signup_user_id = request.session.get('pending_signup_user_id')
        
        user = None
        verification_type = None
        
        if pending_login_user_id:
            user = User.objects.get(id=pending_login_user_id)
            verification_type = 'login'
        elif pending_signup_user_id:
            user = User.objects.get(id=pending_signup_user_id)
            verification_type = 'signup'
        
        # Verify OTP using user model method
        if user and user.verify_otp(otp_code):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Clear session data
            request.session.pop('pending_login_user_id', None)
            request.session.pop('pending_signup_user_id', None)
            
            return redirect('applications:home')
```

**OTP Model Methods:** `accounts/models.py` - `CustomUser` class
```python
def generate_otp(self):
    """Generate a 6-digit OTP and update fields"""
    self.otp_code = ''.join(random.choices(string.digits, k=6))
    self.otp_created_at = timezone.now()
    self.otp_verified = False
    self.save()
    return self.otp_code

def verify_otp(self, code):
    """Validate OTP (must not be expired and must match)"""
    if not self.otp_code or not self.otp_created_at:
        return False
    
    # Check expiration (10 minutes)
    if (timezone.now() - self.otp_created_at).total_seconds() > 600:
        return False
    
    # Check code match
    if self.otp_code == code:
        self.otp_verified = True
        self.otp_code = None  # Clear after success
        self.save()
        return True
    
    return False
```

---

### 4. USER LOGOUT

**URL:** `/accounts/logout/`
**Implementation:** Django's built-in `LogoutView`

```python
# In accounts/urls.py
path('logout/', LogoutView.as_view(), name='logout'),
```

**Functionality:**
- Clears user session data
- Logs out user from Django authentication system
- Redirects to login page (default behavior)
- Clears any pending OTP verification data

---

## 📄 NRC APPLICATION SYSTEM

### 1. NEW NRC APPLICATION

**File:** `applications/views.py` - `apply_nrc` function
**URL:** `/apply/`
**Template:** `templates/applications/apply.html`

```python
@login_required
def apply_nrc(request):
    # Check if user already has a new NRC application
    existing_new_application = NRCApplication.objects.filter(
        user=request.user, 
        application_type='new'
    ).exists()
    
    if existing_new_application:
        messages.warning(request, 'You have already submitted a new NRC application.')
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
```

**Form Fields:** `applications/forms.py` - `NRCApplicationForm`
```python
fields = [
    # Personal Information
    'village', 'district', 'date_of_birth', 'place_of_birth', 'chief_name', 'sex', 'photo',
    
    # Mother's Information
    'mother_full_name', 'mother_village', 'mother_district', 'mother_date_of_birth', 
    'mother_place_of_birth', 'mother_chief_name',
    
    # Father's Information
    'father_full_name', 'father_village', 'father_district', 'father_date_of_birth', 
    'father_place_of_birth', 'father_chief_name',
    
    # Required Documents
    'birth_certificate', 'under_five_card'
]
```

**Key Features:**
- **One Application Rule:** Users can only submit one new NRC application
- **Complete Information:** Collects personal, parents', and document information
- **File Uploads:** Handles birth certificate, under-five card, and photo uploads
- **Validation:** Form validation ensures all required fields are provided

---

### 2. NRC REPLACEMENT APPLICATION

**File:** `applications/views.py` - `apply_replacement` function
**URL:** `/apply-replacement/`
**Template:** `templates/applications/apply_replacement.html`

```python
@login_required
def apply_replacement(request):
    if request.method == 'POST':
        form = NRCReplacementForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.application_type = 'replacement'
            
            # Copy user's existing information from their first application
            first_app = NRCApplication.objects.filter(user=request.user, application_type='new').first()
            if first_app:
                # Copy all personal and family information
                application.village = first_app.village
                application.district = first_app.district
                application.date_of_birth = first_app.date_of_birth
                # ... (copies all fields from original application)
            
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
```

**Replacement Form Fields:** `applications/forms.py` - `NRCReplacementForm`
```python
fields = [
    'old_nrc',              # Old/Damaged NRC document
    'birth_certificate',    # Birth certificate
    'under_five_card',     # Under five card
    'replacement_reason'    # Detailed reason for replacement
]
```

**Key Features:**
- **Data Inheritance:** Copies information from user's original new NRC application
- **Simplified Process:** Only requires documents and replacement reason
- **Multiple Replacements:** Users can apply for multiple replacements if needed
- **Validation:** Requires old NRC document and detailed reason

---

## 📊 APPLICATION MANAGEMENT

### 1. VIEW MY APPLICATIONS

**File:** `applications/views.py` - `my_applications` function
**URL:** `/my-applications/`
**Template:** `templates/applications/my_applications.html`

```python
@login_required
def my_applications(request):
    applications = NRCApplication.objects.filter(user=request.user)
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'applications/my_applications.html', {'page_obj': page_obj})
```

**Features:**
- Shows all user's applications (new and replacement)
- Pagination (10 applications per page)
- Status indicators (pending, approved, rejected)
- Links to detailed application view

---

### 2. APPLICATION DETAIL VIEW

**File:** `applications/views.py` - `application_detail` function
**URL:** `/application/<int:pk>/`
**Template:** `templates/applications/application_detail.html`

```python
@login_required
def application_detail(request, pk):
    application = get_object_or_404(NRCApplication, pk=pk, user=request.user)
    return render(request, 'applications/application_detail.html', {'application': application})
```

**Features:**
- Shows complete application information
- Displays current status and admin notes
- Links to NRC card view (if approved)
- Security: Users can only view their own applications

---

## 🏛️ ADMIN FUNCTIONALITY

### 1. ADMIN DASHBOARD

**File:** `applications/views.py` - `admin_dashboard` function
**URL:** `/admin-dashboard/`
**Template:** `templates/applications/admin_dashboard.html`

```python
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
```

---

### 2. ADMIN APPLICATION REVIEW

**File:** `applications/views.py` - `admin_application_detail` function
**URL:** `/dashboard/application/<int:pk>/`
**Template:** `templates/applications/admin_application_detail.html`

```python
@user_passes_test(is_admin)
def admin_application_detail(request, pk):
    application = get_object_or_404(NRCApplication, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '')
        
        # Update application
        application.status = status
        application.admin_notes = admin_notes
        application.save()
        
        # Generate NRC card if approved and not yet generated
        if status == 'approved' and not application.nrc_front_image:
            try:
                front_path, back_path, nrc_number = generate_nrc_card(application)
                application.nrc_front_image = front_path
                application.nrc_back_image = back_path
                application.nrc_number = nrc_number
                application.nrc_generated_at = timezone.now()
                application.save()
                messages.success(request, f'Application approved and NRC card generated! NRC Number: {nrc_number}')
            except Exception as e:
                messages.warning(request, f'Application approved but NRC card generation failed: {str(e)}')
        
        return redirect('applications:admin_application_detail', pk=pk)
    
    return render(request, 'applications/admin_application_detail.html', {'application': application})
```

**Key Features:**
- **Status Management:** Change application status (pending/approved/rejected)
- **Admin Notes:** Add detailed notes about the application
- **Automatic NRC Generation:** Generates NRC card when application is approved
- **Document Review:** View all uploaded documents
- **User Information:** Complete applicant and family details

---

## 🎫 NRC CARD GENERATION

**File:** `applications/nrc_generator.py` - `generate_nrc_card` function

```python
def generate_nrc_card(application):
    """
    Generate NRC card images (front and back) for approved applications
    """
    # Generate unique NRC number
    nrc_number = generate_nrc_number(application)
    
    # Create front card with photo, personal info, and Zambian coat of arms
    front_image = create_front_card(application, nrc_number)
    
    # Create back card with family information and security features
    back_image = create_back_card(application, nrc_number)
    
    # Save images to media directory
    front_path = save_card_image(front_image, f"nrc_front_{application.id}.png")
    back_path = save_card_image(back_image, f"nrc_back_{application.id}.png")
    
    return front_path, back_path, nrc_number
```

**Features:**
- **Unique NRC Numbers:** Generates unique identification numbers
- **Professional Design:** Zambian coat of arms and official styling
- **Security Features:** Barcodes, signatures, and official formatting
- **Photo Integration:** Includes applicant's photo on front card
- **Family Information:** Parents' details on back card

---

## 📊 REPORTING SYSTEM

### 1. SUMMARY REPORTS

**File:** `applications/views.py` - `summary_report` function
**URL:** `/dashboard/reports/summary/`

```python
@user_passes_test(is_admin)
def summary_report(request):
    # Date range filtering
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    applications = NRCApplication.objects.all()
    if date_from:
        applications = applications.filter(created_at__gte=date_from)
    if date_to:
        applications = applications.filter(created_at__lte=date_to)
    
    # Generate statistics
    total_applications = applications.count()
    new_applications = applications.filter(application_type='new').count()
    replacement_applications = applications.filter(application_type='replacement').count()
    
    # Status distribution
    pending_count = applications.filter(status='pending').count()
    approved_count = applications.filter(status='approved').count()
    rejected_count = applications.filter(status='rejected').count()
    
    # Gender statistics
    male_count = applications.filter(sex='M').count()
    female_count = applications.filter(sex='F').count()
    
    # Top districts
    top_districts = applications.values('district').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Export functionality
    export_format = request.GET.get('export')
    if export_format in ['csv', 'pdf', 'excel', 'word']:
        return ReportsService.get_export_response(context, 'summary', export_format)
    
    return render(request, 'applications/summary_report.html', context)
```

---

### 2. DETAILED REPORTS

**Features:**
- **Advanced Filtering:** Status, type, date range, district
- **Pagination:** 50 records per page
- **Export Options:** CSV, PDF, Excel, Word formats
- **Search Functionality:** Find specific applications
- **Complete Data:** All application fields and user information

---

### 3. EXCEPTION REPORTS

**Identifies:**
- Pending applications older than 30 days
- Approved applications without NRC numbers
- Multiple applications from same user
- Rejected applications without admin notes

---

## 🔒 SECURITY FEATURES

### 1. Authentication Security
- **OTP Verification:** 6-digit codes with 10-minute expiration
- **Admin Bypass:** Staff accounts skip OTP for faster access
- **Session Management:** Secure session handling for pending verifications
- **Password Security:** Django's built-in password validation

### 2. Authorization
- **Login Required:** All application functions require authentication
- **Admin Only:** Administrative functions restricted to staff users
- **User Isolation:** Users can only access their own applications
- **Permission Checks:** `@user_passes_test(is_admin)` decorators

### 3. Data Validation
- **Form Validation:** Server-side validation for all inputs
- **File Upload Security:** Restricted file types and sizes
- **SQL Injection Protection:** Django ORM prevents SQL injection
- **CSRF Protection:** Cross-site request forgery protection enabled

---

## 📧 EMAIL SYSTEM

### Gmail SMTP Configuration
```python
# Force Gmail settings for OTP emails
settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
settings.EMAIL_HOST = 'smtp.gmail.com'
settings.EMAIL_PORT = 587
settings.EMAIL_USE_TLS = True
settings.EMAIL_HOST_USER = 'simoongalaurent427@gmail.com'
settings.EMAIL_HOST_PASSWORD = 'sghuygvzhowzrdmm'  # App-specific password
```

**Features:**
- **Reliable Delivery:** Gmail SMTP for production reliability
- **Fallback System:** Shows OTP in browser if email fails
- **Professional Templates:** Branded email templates
- **Error Handling:** Graceful handling of email failures

---

## 🗄️ DATABASE MODELS

### User Model (`accounts/models.py`)
```python
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    nrc_number = models.CharField(max_length=20, blank=True, unique=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # OTP fields
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
```

### Application Model (`applications/models.py`)
```python
class NRCApplication(models.Model):
    # Application Info
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=20, choices=[('new', 'New NRC'), ('replacement', 'Replacement')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Personal Details
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    chief_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    photo = models.ImageField(upload_to='photos/applicants/')
    
    # Family Information (Mother & Father details)
    # Document uploads (birth certificate, under-five card, old NRC)
    # Generated NRC information
    # Digital signature support
```

---

## 🚀 DEPLOYMENT CONSIDERATIONS

### Production Settings
- **Debug Mode:** Set `DEBUG = False` in production
- **Allowed Hosts:** Configure proper domain names
- **Static Files:** Use WhiteNoise or CDN for static file serving
- **Database:** PostgreSQL recommended for production
- **Email:** Gmail SMTP with app-specific passwords

### Security Checklist
- **HTTPS:** Enable SSL/TLS encryption
- **CSRF Protection:** Enabled by default
- **SQL Injection:** Protected by Django ORM
- **File Upload Security:** Validate file types and sizes
- **Session Security:** Secure session configuration

---

## 📞 SUPPORT AND MAINTENANCE

### Common Issues
1. **OTP Email Delivery:** Check Gmail SMTP credentials
2. **File Upload Errors:** Verify media directory permissions
3. **Database Migrations:** Run `python manage.py migrate`
4. **Static Files:** Run `python manage.py collectstatic`

### Monitoring
- **Application Logs:** Monitor Django logs for errors
- **Email Delivery:** Track OTP email success rates
- **Database Performance:** Monitor query performance
- **User Activity:** Track login and application submission rates

---

## 🔧 DEVELOPMENT SETUP

### Required Dependencies
```txt
Django>=4.2.0
Pillow>=9.0.0
django-allauth>=0.54.0
reportlab>=3.6.0
openpyxl>=3.1.0
python-docx>=0.8.11
xlsxwriter>=3.1.0
```

### Environment Variables
```env
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
GEMINI_API_KEY=your-gemini-key (optional)
```

### Initial Setup Commands
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver
```

---

This comprehensive guide covers all major functionality in the Zambian NRC System. Each section provides code examples, explanations, and implementation details for developers and system administrators.