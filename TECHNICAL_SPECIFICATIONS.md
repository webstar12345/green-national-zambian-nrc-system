# ⚙️ NRC System Technical Specifications
## Complete Technical Documentation

---

## 🏗️ System Architecture

### Technology Stack

#### Backend Framework
- **Django 4.2.7**: Python web framework
- **Python 3.8+**: Programming language
- **Django REST Framework**: API development
- **Gunicorn**: WSGI HTTP Server
- **Whitenoise**: Static file serving

#### Frontend Technologies
- **HTML5**: Semantic markup
- **CSS3**: Styling and animations
- **JavaScript (ES6+)**: Interactive functionality
- **Tailwind CSS**: Utility-first CSS framework
- **Progressive Web App (PWA)**: Mobile-first design

#### Database Systems
- **Development**: SQLite 3.x
- **Production**: PostgreSQL 12+
- **ORM**: Django ORM with migrations
- **Backup**: Automated daily backups

#### Authentication & Security
- **Django Authentication**: Built-in user management
- **OTP System**: Email-based two-factor authentication
- **Google OAuth 2.0**: Social authentication
- **CSRF Protection**: Cross-site request forgery prevention
- **XSS Protection**: Cross-site scripting prevention

#### Third-Party Integrations
- **Gmail SMTP**: Email delivery service
- **Cloudinary**: Media file storage and optimization
- **Google AI (Gemini)**: AI assistant functionality
- **Render.com**: Production hosting platform

---

## 📊 Database Schema

### Core Models

#### CustomUser Model
```python
class CustomUser(AbstractUser):
    # Inherited from AbstractUser
    username = CharField(max_length=150, unique=True)
    email = EmailField(unique=True)
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    date_joined = DateTimeField(auto_now_add=True)
    last_login = DateTimeField(null=True, blank=True)
    
    # Custom fields
    phone_number = CharField(max_length=20, blank=True)
    profile_image = CloudinaryField('image', null=True, blank=True)
    otp_code = CharField(max_length=6, blank=True)
    otp_created_at = DateTimeField(null=True, blank=True)
    
    # Methods
    def generate_otp(self) -> str
    def verify_otp(self, code: str) -> bool
    def get_full_name(self) -> str
```

#### NRCApplication Model
```python
class NRCApplication(models.Model):
    APPLICATION_TYPES = [
        ('new', 'New NRC'),
        ('replacement', 'Replacement NRC'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    # Primary fields
    id = AutoField(primary_key=True)
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    application_type = CharField(max_length=20, choices=APPLICATION_TYPES)
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Personal information
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    date_of_birth = DateField()
    sex = CharField(max_length=1, choices=SEX_CHOICES)
    nationality = CharField(max_length=50, default='Zambian')
    
    # Address information
    province = CharField(max_length=100)
    district = CharField(max_length=100)
    constituency = CharField(max_length=100)
    ward = CharField(max_length=100)
    village = CharField(max_length=100)
    
    # Contact information
    phone_number = CharField(max_length=20)
    email = EmailField()
    
    # Documents
    birth_certificate = CloudinaryField('image')
    proof_of_residence = CloudinaryField('image')
    passport_photo = CloudinaryField('image')
    signature = TextField()  # Base64 encoded signature
    
    # NRC details
    nrc_number = CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Replacement specific
    replacement_reason = CharField(max_length=200, blank=True)
    previous_nrc_number = CharField(max_length=20, blank=True)
    
    # Administrative
    admin_notes = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    # Methods
    def generate_nrc_number(self) -> str
    def get_status_display(self) -> str
    def get_application_type_display(self) -> str
```

### Database Indexes
```sql
-- Performance optimization indexes
CREATE INDEX idx_applications_status ON applications_nrcapplication(status);
CREATE INDEX idx_applications_created ON applications_nrcapplication(created_at);
CREATE INDEX idx_applications_user ON applications_nrcapplication(user_id);
CREATE INDEX idx_applications_nrc_number ON applications_nrcapplication(nrc_number);
CREATE INDEX idx_users_email ON accounts_customuser(email);
CREATE INDEX idx_users_username ON accounts_customuser(username);
```

---

## 🔌 API Endpoints

### Authentication Endpoints

#### User Registration
```http
POST /accounts/signup/
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
}

Response: 201 Created
{
    "message": "Account created successfully",
    "user_id": "integer",
    "otp_required": true
}
```

#### User Login
```http
POST /accounts/login/
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}

Response: 200 OK (Regular User)
{
    "message": "OTP sent to email",
    "otp_required": true,
    "email": "string"
}

Response: 200 OK (Admin User)
{
    "message": "Login successful",
    "redirect_url": "/admin-dashboard/",
    "user_type": "admin"
}
```

#### OTP Verification
```http
POST /accounts/otp/verify/
Content-Type: application/json

{
    "otp_code": "string"
}

Response: 200 OK
{
    "message": "Verification successful",
    "redirect_url": "/dashboard/"
}
```

### Application Endpoints

#### Submit Application
```http
POST /applications/apply/
Content-Type: multipart/form-data

{
    "application_type": "new|replacement",
    "first_name": "string",
    "last_name": "string",
    "date_of_birth": "YYYY-MM-DD",
    "sex": "M|F",
    "province": "string",
    "district": "string",
    "constituency": "string",
    "ward": "string",
    "village": "string",
    "phone_number": "string",
    "email": "string",
    "birth_certificate": "file",
    "proof_of_residence": "file",
    "passport_photo": "file",
    "signature": "base64_string"
}

Response: 201 Created
{
    "application_id": "integer",
    "message": "Application submitted successfully",
    "reference_number": "string"
}
```

#### Get User Applications
```http
GET /applications/my-applications/

Response: 200 OK
{
    "applications": [
        {
            "id": "integer",
            "application_type": "string",
            "status": "string",
            "created_at": "datetime",
            "nrc_number": "string|null"
        }
    ]
}
```

### Admin Endpoints

#### Get Pending Applications
```http
GET /admin/applications/pending/

Response: 200 OK
{
    "applications": [
        {
            "id": "integer",
            "user": {
                "username": "string",
                "email": "string",
                "full_name": "string"
            },
            "application_type": "string",
            "created_at": "datetime",
            "days_pending": "integer"
        }
    ]
}
```

#### Approve Application
```http
POST /admin/applications/{id}/approve/
Content-Type: application/json

{
    "admin_notes": "string"
}

Response: 200 OK
{
    "message": "Application approved",
    "nrc_number": "string"
}
```

#### Reject Application
```http
POST /admin/applications/{id}/reject/
Content-Type: application/json

{
    "reason": "string",
    "admin_notes": "string"
}

Response: 200 OK
{
    "message": "Application rejected"
}
```

### Reporting Endpoints

#### Generate Summary Report
```http
GET /reports/summary/
Query Parameters:
- date_from: YYYY-MM-DD (optional)
- date_to: YYYY-MM-DD (optional)
- format: pdf|excel|word|csv (optional)

Response: 200 OK
{
    "total_applications": "integer",
    "pending_count": "integer",
    "approved_count": "integer",
    "rejected_count": "integer",
    "processing_rate": "float",
    "top_districts": "array"
}
```

---

## 🔒 Security Implementation

### Authentication Security

#### OTP System
```python
class OTPService:
    @staticmethod
    def generate_otp_code() -> str:
        """Generate 6-digit numeric OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def send_otp_email(email: str, otp_code: str, user_name: str) -> bool:
        """Send OTP via Gmail SMTP with HTML template"""
        # Implementation with error handling and logging
    
    @staticmethod
    def is_otp_expired(otp_created_at: datetime, expiry_minutes: int = 10) -> bool:
        """Check if OTP has expired"""
        # Implementation with timezone awareness
```

#### Admin Bypass Logic
```python
def form_valid(self, form):
    """Custom login with admin bypass"""
    user = authenticate(username=username, password=password)
    
    if user.is_staff or user.is_superuser:
        # Admin users bypass OTP
        login(self.request, user)
        return redirect('applications:home')
    else:
        # Regular users require OTP
        otp_code = user.generate_otp()
        # Send OTP and redirect to verification
```

### Data Protection

#### Input Validation
```python
class NRCApplicationForm(forms.ModelForm):
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        # Validate phone number format
        if not re.match(r'^\+260[0-9]{9}$', phone):
            raise ValidationError('Invalid phone number format')
        return phone
    
    def clean_birth_certificate(self):
        file = self.cleaned_data['birth_certificate']
        # Validate file type and size
        if file.size > 5 * 1024 * 1024:  # 5MB limit
            raise ValidationError('File too large')
        return file
```

#### SQL Injection Prevention
```python
# Django ORM automatically prevents SQL injection
applications = NRCApplication.objects.filter(
    status='pending',
    created_at__gte=date_from
).select_related('user')

# Parameterized queries for raw SQL (if needed)
cursor.execute(
    "SELECT * FROM applications WHERE status = %s AND created_at >= %s",
    [status, date_from]
)
```

#### XSS Prevention
```html
<!-- Django templates auto-escape by default -->
<p>{{ user.first_name|escape }}</p>

<!-- For trusted HTML content -->
<div>{{ admin_notes|safe }}</div>

<!-- Custom escaping -->
<script>
    var userName = "{{ user.username|escapejs }}";
</script>
```

### File Upload Security

#### File Validation
```python
def validate_image_file(file):
    """Validate uploaded image files"""
    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError('Invalid file type')
    
    # Check file size (5MB limit)
    if file.size > 5 * 1024 * 1024:
        raise ValidationError('File too large')
    
    # Check file content (basic magic number check)
    file.seek(0)
    header = file.read(512)
    file.seek(0)
    
    # Validate image headers
    if not any(header.startswith(sig) for sig in [
        b'\xff\xd8\xff',  # JPEG
        b'\x89PNG\r\n\x1a\n',  # PNG
        b'%PDF-'  # PDF
    ]):
        raise ValidationError('Invalid file format')
```

#### Cloudinary Integration
```python
# Secure file upload to Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
    'SECURE': True,
    'FOLDER': 'nrc-documents',
    'TRANSFORMATION': {
        'quality': 'auto:good',
        'fetch_format': 'auto'
    }
}
```

---

## 📧 Email System Configuration

### Gmail SMTP Setup
```python
# Email configuration in settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  # App password
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
```

### Email Templates

#### OTP Verification Email
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>NRC System - Verification Code</title>
    <style>
        .container { max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }
        .header { background: #2D5016; color: white; padding: 20px; text-align: center; }
        .content { padding: 30px; background: #f9f9f9; }
        .otp-code { font-size: 32px; font-weight: bold; color: #2D5016; text-align: center; 
                   background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .footer { padding: 20px; text-align: center; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🇿🇲 NRC Zambia</h1>
            <p>National Registration Card System</p>
        </div>
        <div class="content">
            <h2>Hello {{ user_name }},</h2>
            <p>Your verification code for the NRC system is:</p>
            <div class="otp-code">{{ otp_code }}</div>
            <p><strong>Important:</strong></p>
            <ul>
                <li>This code expires in 10 minutes</li>
                <li>Do not share this code with anyone</li>
                <li>If you didn't request this code, please ignore this email</li>
            </ul>
        </div>
        <div class="footer">
            <p>© 2025 Republic of Zambia - National Registration Department</p>
            <p>This is an automated message, please do not reply.</p>
        </div>
    </div>
</body>
</html>
```

### Email Delivery Monitoring
```python
class EmailService:
    @staticmethod
    def send_with_retry(subject, message, recipient_list, max_retries=3):
        """Send email with retry logic"""
        for attempt in range(max_retries):
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                logger.info(f"Email sent successfully to {recipient_list}")
                return True
            except Exception as e:
                logger.error(f"Email attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"All email attempts failed for {recipient_list}")
                    return False
                time.sleep(2 ** attempt)  # Exponential backoff
        return False
```

---

## 📊 Reporting System Architecture

### Report Generation Service
```python
class ReportsService:
    @staticmethod
    def get_summary_report_data(date_from=None, date_to=None):
        """Generate summary statistics"""
        queryset = NRCApplication.objects.all()
        
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        
        return {
            'total_applications': queryset.count(),
            'pending_count': queryset.filter(status='pending').count(),
            'approved_count': queryset.filter(status='approved').count(),
            'rejected_count': queryset.filter(status='rejected').count(),
            'processing_rate': calculate_processing_rate(queryset),
            'top_districts': g