# 🇿🇲 Zambian National Registration Card (NRC) System
## Complete System Documentation & User Guide

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [User Guide](#user-guide)
3. [Admin Guide](#admin-guide)
4. [Technical Documentation](#technical-documentation)
5. [Installation & Setup](#installation--setup)
6. [API Reference](#api-reference)
7. [Troubleshooting](#troubleshooting)
8. [Security Features](#security-features)

---

## 🎯 System Overview

### Purpose
The Zambian NRC System is a comprehensive digital platform for managing National Registration Card applications, designed to streamline the process of applying for, processing, and issuing NRC documents for Zambian citizens.

### Key Features
- **Digital NRC Applications** - Online application submission
- **OTP Email Verification** - Secure two-factor authentication
- **Admin Dashboard** - Comprehensive management interface
- **Reporting System** - Advanced analytics and exports
- **Multi-format Exports** - PDF, Excel, Word, CSV reports
- **Google OAuth Integration** - Social login capability
- **Progressive Web App (PWA)** - Mobile-friendly interface
- **AI Assistant** - Intelligent chat support
- **Barcode & Signature System** - Digital verification
- **Multi-language Support** - English and local languages

### System Architecture
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Backend**: Django 4.2.7 (Python)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django Auth + OTP + Google OAuth
- **Email**: Gmail SMTP with app passwords
- **Hosting**: Render.com (Production)
- **Storage**: Cloudinary (Media files)

---

## 👤 User Guide

### Getting Started

#### 1. Account Registration
1. **Visit the System**: Go to the NRC system website
2. **Click "Sign Up"**: Located on the login page
3. **Fill Registration Form**:
   - Username (unique identifier)
   - Email address (for OTP verification)
   - Password (minimum 8 characters)
   - First Name and Last Name
4. **Email Verification**: 
   - Check your email for OTP code
   - Enter the 6-digit code to verify your account
5. **Account Activated**: You can now login and apply for NRC

#### 2. Login Process
1. **Regular Users**:
   - Enter username and password
   - Receive OTP code via email
   - Enter OTP to complete login
2. **Google Login**:
   - Click "Sign in with Google"
   - Authorize with your Google account
   - Complete OTP verification if required

#### 3. Applying for NRC

##### New NRC Application
1. **Navigate to Apply**: Click "Apply for NRC" from dashboard
2. **Select Application Type**: Choose "New NRC"
3. **Personal Information**:
   - Full names (as they should appear on NRC)
   - Date of birth
   - Gender
   - Nationality (Zambian)
4. **Address Information**:
   - Province
   - District
   - Constituency
   - Ward
   - Village/Area
5. **Contact Information**:
   - Phone number
   - Email address
   - Alternative contact
6. **Supporting Documents**:
   - Birth certificate (upload image)
   - Proof of residence
   - Passport photo
7. **Digital Signature**: Sign using the signature pad
8. **Review & Submit**: Verify all information before submission

##### Replacement NRC Application
1. **Select "Replacement NRC"** from application types
2. **Reason for Replacement**:
   - Lost NRC
   - Damaged NRC
   - Name change
   - Other (specify)
3. **Previous NRC Details**:
   - Previous NRC number (if known)
   - Date of issue
4. **Complete remaining steps** as per new application

#### 4. Tracking Your Application
1. **Dashboard Overview**: View application status summary
2. **My Applications**: Detailed list of all applications
3. **Application Details**: Click on any application to view:
   - Current status (Pending/Approved/Rejected)
   - Submission date
   - Processing timeline
   - Admin notes (if any)
   - Download options (if approved)

#### 5. Profile Management
1. **View Profile**: Access personal information
2. **Edit Profile**: Update contact details and personal info
3. **Change Password**: Security settings
4. **Upload Profile Picture**: Personalize your account

---

## 👨‍💼 Admin Guide

### Admin Access
- **Login**: Admins bypass OTP verification for faster access
- **Dashboard**: Comprehensive overview of system statistics
- **Permissions**: Full access to all system functions

### Application Management

#### 1. Application Review
1. **Pending Applications**: Review new submissions
2. **Application Details**: 
   - View all submitted information
   - Check uploaded documents
   - Verify digital signatures
3. **Decision Making**:
   - **Approve**: Generate NRC number and approve
   - **Reject**: Provide reason for rejection
   - **Request More Info**: Ask for additional documents

#### 2. User Management
1. **User List**: View all registered users
2. **User Details**: Access complete user profiles
3. **Account Actions**:
   - Activate/Deactivate accounts
   - Reset passwords
   - Modify user permissions

#### 3. Reporting System

##### Summary Reports
- **Overview Statistics**: Total applications, approval rates
- **Demographic Analysis**: Age, gender, location distributions
- **Performance Metrics**: Processing times, efficiency rates
- **Export Options**: PDF, Excel, Word, CSV

##### Detailed Reports
- **Application Listings**: Filterable by status, date, location
- **Custom Date Ranges**: Specific time period analysis
- **Search Functionality**: Find specific applications
- **Bulk Operations**: Mass approve/reject capabilities

##### Exception Reports
- **Problem Applications**: Long pending, missing information
- **System Issues**: Duplicate applications, data inconsistencies
- **Priority Actions**: Critical items requiring attention

#### 4. System Administration
1. **Site Configuration**: Update system settings
2. **Email Templates**: Customize notification messages
3. **Security Settings**: Manage authentication requirements
4. **Backup Management**: Data export and backup procedures

---

## 🔧 Technical Documentation

### System Requirements

#### Development Environment
- **Python**: 3.8 or higher
- **Django**: 4.2.7
- **Database**: SQLite (included)
- **Node.js**: For frontend build tools (optional)

#### Production Environment
- **Server**: Linux/Windows server
- **Python**: 3.8+
- **Database**: PostgreSQL 12+
- **Web Server**: Nginx + Gunicorn
- **SSL Certificate**: Required for HTTPS

### Database Schema

#### User Model (CustomUser)
```python
- id: Primary Key
- username: Unique identifier
- email: Email address
- first_name: User's first name
- last_name: User's last name
- is_staff: Admin flag
- is_superuser: Superuser flag
- date_joined: Registration date
- last_login: Last login timestamp
- otp_code: Current OTP code
- otp_created_at: OTP generation time
```

#### NRC Application Model
```python
- id: Primary Key
- user: Foreign Key to User
- application_type: 'new' or 'replacement'
- status: 'pending', 'approved', 'rejected'
- first_name: Applicant's first name
- last_name: Applicant's last name
- date_of_birth: Birth date
- sex: Gender (M/F)
- nationality: Country
- province: Province name
- district: District name
- constituency: Constituency name
- ward: Ward name
- village: Village/Area name
- phone_number: Contact number
- nrc_number: Generated NRC number (if approved)
- created_at: Application date
- updated_at: Last modification date
- admin_notes: Admin comments
```

### API Endpoints

#### Authentication
- `POST /accounts/login/` - User login
- `POST /accounts/signup/` - User registration
- `POST /accounts/otp/verify/` - OTP verification
- `POST /accounts/logout/` - User logout

#### Applications
- `GET /applications/` - List user applications
- `POST /applications/apply/` - Submit new application
- `GET /applications/{id}/` - Application details
- `PUT /applications/{id}/` - Update application

#### Admin
- `GET /admin-dashboard/` - Admin dashboard
- `GET /dashboard/reports/` - Reports interface
- `GET /dashboard/applications/` - Application management
- `POST /dashboard/applications/{id}/approve/` - Approve application
- `POST /dashboard/applications/{id}/reject/` - Reject application

### Security Features

#### Authentication Security
1. **OTP Verification**: 6-digit codes via email
2. **Admin Bypass**: Admins skip OTP for efficiency
3. **Session Management**: Secure session handling
4. **Password Requirements**: Minimum 8 characters
5. **Account Lockout**: Protection against brute force

#### Data Security
1. **HTTPS Encryption**: All data transmission encrypted
2. **Database Security**: Parameterized queries prevent SQL injection
3. **File Upload Security**: Validated file types and sizes
4. **CSRF Protection**: Cross-site request forgery prevention
5. **XSS Protection**: Cross-site scripting prevention

#### Privacy Protection
1. **Data Minimization**: Only necessary data collected
2. **Access Controls**: Role-based permissions
3. **Audit Logging**: All actions logged for accountability
4. **Data Retention**: Configurable data retention policies

---

## 🚀 Installation & Setup

### Local Development Setup

#### 1. Prerequisites
```bash
# Install Python 3.8+
python --version

# Install Git
git --version
```

#### 2. Clone Repository
```bash
git clone <repository-url>
cd nrc-system
```

#### 3. Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# Required settings:
# - SECRET_KEY
# - EMAIL_HOST_USER
# - EMAIL_HOST_PASSWORD
# - GOOGLE_CLIENT_ID (optional)
# - GOOGLE_CLIENT_SECRET (optional)
```

#### 6. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata sample_data.json
```

#### 7. Run Development Server
```bash
python manage.py runserver
```

### Production Deployment

#### 1. Server Setup (Ubuntu/Debian)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib

# Install Node.js (for frontend builds)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 2. Database Configuration
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE nrc_system;
CREATE USER nrc_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE nrc_system TO nrc_user;
\q
```

#### 3. Application Deployment
```bash
# Clone repository
git clone <repository-url> /var/www/nrc-system
cd /var/www/nrc-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Configure environment
cp .env.example .env
# Edit .env with production settings

# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

#### 4. Gunicorn Configuration
```bash
# Create gunicorn service file
sudo nano /etc/systemd/system/nrc-system.service
```

```ini
[Unit]
Description=NRC System Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/nrc-system
ExecStart=/var/www/nrc-system/venv/bin/gunicorn --workers 3 --bind unix:/var/www/nrc-system/nrc_system.sock nrc_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 5. Nginx Configuration
```bash
# Create Nginx site configuration
sudo nano /etc/nginx/sites-available/nrc-system
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/nrc-system;
    }
    
    location /media/ {
        root /var/www/nrc-system;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/nrc-system/nrc_system.sock;
    }
}
```

#### 6. SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. OTP Email Not Received
**Problem**: Users not receiving OTP verification emails

**Solutions**:
1. Check spam/junk folder
2. Verify email configuration in `.env`
3. Test SMTP connection:
```bash
python test_gmail_smtp.py
```
4. Generate new Gmail app password if needed

#### 2. Admin Login Issues
**Problem**: Admin users unable to access dashboard

**Solutions**:
1. Verify admin privileges:
```bash
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(username='admin')
>>> user.is_staff = True
>>> user.is_superuser = True
>>> user.save()
```

#### 3. Reports Generation Errors
**Problem**: Error when generating reports

**Solutions**:
1. Check database connectivity
2. Verify report service syntax:
```bash
python test_reports_fix.py
```
3. Clear cache and restart server

#### 4. File Upload Issues
**Problem**: Unable to upload documents

**Solutions**:
1. Check file size limits in settings
2. Verify media directory permissions
3. Ensure Cloudinary configuration (if used)

#### 5. Google OAuth Problems
**Problem**: Google login not working

**Solutions**:
1. Verify Google Cloud Console settings
2. Check redirect URIs configuration
3. Update site domain:
```bash
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> site = Site.objects.get_current()
>>> site.domain = 'your-domain.com'
>>> site.save()
```

### Performance Optimization

#### 1. Database Optimization
```python
# Add database indexes
python manage.py dbshell
CREATE INDEX idx_applications_status ON applications_nrcapplication(status);
CREATE INDEX idx_applications_created ON applications_nrcapplication(created_at);
```

#### 2. Caching Configuration
```python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

#### 3. Static File Optimization
```bash
# Compress static files
python manage.py compress

# Use CDN for static files (production)
# Configure Cloudinary or AWS S3
```

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks

#### Daily
- Monitor system logs for errors
- Check email delivery status
- Review pending applications

#### Weekly
- Database backup
- Security updates check
- Performance monitoring

#### Monthly
- Full system backup
- User account cleanup
- Security audit

### Support Contacts
- **Technical Support**: [Your IT Team]
- **System Administrator**: [Admin Contact]
- **Emergency Contact**: [24/7 Support]

### Documentation Updates
This documentation should be updated whenever:
- New features are added
- System configurations change
- User workflows are modified
- Security procedures are updated

---

## 📄 License & Legal

### System License
This NRC system is proprietary software developed for the Zambian government. All rights reserved.

### Data Protection
The system complies with:
- Zambian Data Protection Act
- International privacy standards
- Government security requirements

### Terms of Use
Users must agree to:
- Provide accurate information
- Use system for legitimate purposes only
- Maintain account security
- Report security issues promptly

---

**Document Version**: 1.0  
**Last Updated**: December 15, 2025  
**Next Review**: March 15, 2026

---

*This documentation is maintained by the NRC System Development Team. For updates or corrections, please contact the system administrator.*