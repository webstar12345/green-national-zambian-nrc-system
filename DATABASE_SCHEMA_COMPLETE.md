# 🗄️ NRC System Database Schema - Complete Documentation

## 📊 Database Overview
The NRC System uses a relational database with two main models: **CustomUser** (accounts) and **NRCApplication** (applications), plus Django's built-in authentication tables.

## 🏗️ Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           NRC SYSTEM DATABASE SCHEMA                            │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐         ┌─────────────────────────────────────────────┐
│      CustomUser         │   1:N   │           NRCApplication                    │
│      (accounts)         │◄────────│          (applications)                     │
├─────────────────────────┤         ├─────────────────────────────────────────────┤
│ PK: id (AutoField)      │         │ PK: id (AutoField)                          │
│ username (CharField)    │         │ FK: user_id → CustomUser.id                 │
│ email (EmailField)      │         │ application_type (CharField)                │
│ first_name (CharField)  │         │ status (CharField)                          │
│ last_name (CharField)   │         │ created_at (DateTimeField)                  │
│ password (CharField)    │         │ updated_at (DateTimeField)                  │
│ is_staff (BooleanField) │         │ village (CharField)                         │
│ is_active (BooleanField)│         │ district (CharField)                        │
│ is_superuser (Boolean)  │         │ date_of_birth (DateField)                   │
│ date_joined (DateTime)  │         │ place_of_birth (CharField)                  │
│ last_login (DateTime)   │         │ chief_name (CharField)                      │
│ phone_number (CharField)│         │ sex (CharField)                             │
│ nrc_number (CharField)  │         │ photo (ImageField)                          │
│ profile_image (Image)   │         │ mother_full_name (CharField)                │
│ bio (TextField)         │         │ mother_village (CharField)                  │
│ otp_code (CharField)    │         │ mother_district (CharField)                 │
│ otp_created_at (DateTime│         │ mother_date_of_birth (DateField)            │
│ otp_verified (Boolean)  │         │ mother_place_of_birth (CharField)           │
└─────────────────────────┘         │ mother_chief_name (CharField)               │
                                    │ father_full_name (CharField)                │
┌─────────────────────────┐         │ father_village (CharField)                  │
│    Django Built-in      │         │ father_district (CharField)                 │
│    Auth Tables          │         │ father_date_of_birth (DateField)            │
├─────────────────────────┤         │ father_place_of_birth (CharField)           │
│ auth_group              │         │ father_chief_name (CharField)               │
│ auth_group_permissions  │         │ birth_certificate (FileField)              │
│ auth_permission         │         │ under_five_card (FileField)                 │
│ django_content_type     │         │ old_nrc (FileField)                         │
│ django_migrations       │         │ replacement_reason (TextField)              │
│ django_session          │         │ admin_notes (TextField)                     │
│ django_site             │         │ nrc_number (CharField)                      │
│ socialaccount_*         │         │ nrc_front_image (CharField)                 │
└─────────────────────────┘         │ nrc_back_image (CharField)                  │
                                    │ nrc_generated_at (DateTimeField)            │
                                    │ digital_signature (TextField)               │
                                    └─────────────────────────────────────────────┘
```

## 📋 Table Definitions

### 1. **accounts_customuser** (User Management)

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| `id` | AutoField | PRIMARY KEY | Unique user identifier |
| `username` | CharField(150) | UNIQUE, NOT NULL | Login username |
| `email` | EmailField(254) | NOT NULL | User email address |
| `first_name` | CharField(150) | | User's first name |
| `last_name` | CharField(150) | | User's last name |
| `password` | CharField(128) | NOT NULL | Hashed password |
| `is_staff` | BooleanField | DEFAULT FALSE | Admin access flag |
| `is_active` | BooleanField | DEFAULT TRUE | Account active status |
| `is_superuser` | BooleanField | DEFAULT FALSE | Superuser privileges |
| `date_joined` | DateTimeField | AUTO NOW ADD | Account creation date |
| `last_login` | DateTimeField | NULLABLE | Last login timestamp |
| `phone_number` | CharField(15) | NULLABLE | Contact phone number |
| `nrc_number` | CharField(20) | UNIQUE, NULLABLE | User's NRC number |
| `profile_image` | ImageField | NULLABLE | Profile photo |
| `bio` | TextField(500) | NULLABLE | User biography |
| `otp_code` | CharField(6) | NULLABLE | Temporary OTP code |
| `otp_created_at` | DateTimeField | NULLABLE | OTP generation time |
| `otp_verified` | BooleanField | DEFAULT FALSE | OTP verification status |

### 2. **applications_nrcapplication** (NRC Applications)

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| `id` | AutoField | PRIMARY KEY | Unique application ID |
| `user_id` | ForeignKey | NOT NULL, CASCADE | Reference to CustomUser |
| `application_type` | CharField(20) | NOT NULL | 'new' or 'replacement' |
| `status` | CharField(20) | DEFAULT 'pending' | Application status |
| `created_at` | DateTimeField | AUTO NOW ADD | Application submission date |
| `updated_at` | DateTimeField | AUTO NOW | Last modification date |
| `village` | CharField(100) | NOT NULL | Applicant's village |
| `district` | CharField(100) | DEFAULT 'Not provided' | Applicant's district |
| `date_of_birth` | DateField | NOT NULL | Applicant's birth date |
| `place_of_birth` | CharField(100) | NOT NULL | Birth location |
| `chief_name` | CharField(100) | NOT NULL | Traditional authority |
| `sex` | CharField(10) | DEFAULT 'M' | Gender (M/F) |
| `photo` | ImageField | NULLABLE | Passport photo |
| `mother_full_name` | CharField(200) | DEFAULT 'Not provided' | Mother's name |
| `mother_village` | CharField(100) | NOT NULL | Mother's village |
| `mother_district` | CharField(100) | DEFAULT 'Not provided' | Mother's district |
| `mother_date_of_birth` | DateField | NOT NULL | Mother's birth date |
| `mother_place_of_birth` | CharField(100) | NOT NULL | Mother's birth place |
| `mother_chief_name` | CharField(100) | NOT NULL | Mother's chief |
| `father_full_name` | CharField(200) | DEFAULT 'Not provided' | Father's name |
| `father_village` | CharField(100) | NOT NULL | Father's village |
| `father_district` | CharField(100) | DEFAULT 'Not provided' | Father's district |
| `father_date_of_birth` | DateField | NOT NULL | Father's birth date |
| `father_place_of_birth` | CharField(100) | NOT NULL | Father's birth place |
| `father_chief_name` | CharField(100) | NOT NULL | Father's chief |
| `birth_certificate` | FileField | NOT NULL | Birth certificate document |
| `under_five_card` | FileField | NOT NULL | Under-5 card document |
| `old_nrc` | FileField | NULLABLE | Old NRC (for replacements) |
| `replacement_reason` | TextField | NULLABLE | Reason for replacement |
| `admin_notes` | TextField | NULLABLE | Administrative notes |
| `nrc_number` | CharField(20) | UNIQUE, NULLABLE | Generated NRC number |
| `nrc_front_image` | CharField(255) | NULLABLE | Front card image path |
| `nrc_back_image` | CharField(255) | NULLABLE | Back card image path |
| `nrc_generated_at` | DateTimeField | NULLABLE | Card generation timestamp |
| `digital_signature` | TextField | NULLABLE | Base64 encoded signature |

## 🔗 Relationships & Constraints

### **Primary Relationships**

1. **CustomUser → NRCApplication** (One-to-Many)
   ```sql
   CustomUser.id ←→ NRCApplication.user_id
   ```
   - **Relationship**: One user can have multiple NRC applications
   - **Constraint**: CASCADE DELETE (if user deleted, applications deleted)
   - **Business Rule**: Users can apply for new NRC and replacements

### **Indexes & Performance**

```sql
-- Automatic indexes created by Django
CREATE INDEX accounts_customuser_username ON accounts_customuser(username);
CREATE INDEX accounts_customuser_email ON accounts_customuser(email);
CREATE INDEX accounts_customuser_nrc_number ON accounts_customuser(nrc_number);
CREATE INDEX applications_nrcapplication_user_id ON applications_nrcapplication(user_id);
CREATE INDEX applications_nrcapplication_status ON applications_nrcapplication(status);
CREATE INDEX applications_nrcapplication_created_at ON applications_nrcapplication(created_at);
CREATE INDEX applications_nrcapplication_nrc_number ON applications_nrcapplication(nrc_number);
```

## 👥 User Types & Permissions

### **1. Regular Users (Citizens)**
```python
is_staff = False
is_superuser = False
is_active = True
```
**Permissions:**
- ✅ Create NRC applications
- ✅ View own applications
- ✅ Add digital signatures
- ✅ Download own NRC cards
- ❌ Access admin functions

### **2. Staff Members (Government Officers)**
```python
is_staff = True
is_superuser = False
is_active = True
```
**Permissions:**
- ✅ All regular user permissions
- ✅ Access admin dashboard
- ✅ View all applications
- ✅ Approve/reject applications
- ✅ Generate NRC cards
- ✅ View reports
- ❌ User management
- ❌ System configuration

### **3. Superusers (System Administrators)**
```python
is_staff = True
is_superuser = True
is_active = True
```
**Permissions:**
- ✅ All staff permissions
- ✅ User management (create/edit/delete users)
- ✅ System configuration
- ✅ Database access
- ✅ Django admin access
- ✅ All system functions

## 📊 Data Flow & Business Logic

### **Application Lifecycle**
```
1. User Registration → CustomUser created
2. User Login → OTP verification
3. Application Submission → NRCApplication created (status: 'pending')
4. Admin Review → Status updated to 'approved'/'rejected'
5. NRC Generation → nrc_number, images generated
6. Digital Signature → signature added, card regenerated
7. Card Download → User accesses final NRC card
```

### **Status Transitions**
```
pending → approved → [NRC Generated] → [Signature Added] → Complete
pending → rejected → End
```

## 🔐 Security Features

### **Authentication & Authorization**
- **Password Hashing**: Django's PBKDF2 algorithm
- **OTP Verification**: 6-digit codes with 10-minute expiry
- **Session Management**: Django sessions with CSRF protection
- **Permission System**: Django's built-in permissions

### **Data Protection**
- **File Upload Security**: Validated file types and sizes
- **SQL Injection Prevention**: Django ORM parameterized queries
- **XSS Protection**: Django template auto-escaping
- **CSRF Protection**: Built-in CSRF middleware

## 📈 Performance Considerations

### **Query Optimization**
```python
# Efficient queries used in views
applications = NRCApplication.objects.select_related('user').filter(status='pending')
user_apps = request.user.nrcapplication_set.all().order_by('-created_at')
```

### **File Storage**
- **Images**: Stored in `media/` directory
- **Documents**: Organized by type in subdirectories
- **Signatures**: Base64 encoded in database (small size)

### **Caching Strategy**
- **Static Files**: Whitenoise compression
- **Database**: Connection pooling
- **Sessions**: Database-backed sessions

## 🗃️ Sample Data Structure

### **CustomUser Example**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_staff": false,
  "phone_number": "+260971234567",
  "nrc_number": null,
  "otp_verified": true
}
```

### **NRCApplication Example**
```json
{
  "id": 1,
  "user_id": 1,
  "application_type": "new",
  "status": "approved",
  "village": "Chilekani",
  "district": "Sinda",
  "date_of_birth": "1996-02-02",
  "sex": "M",
  "nrc_number": "Z 12345678",
  "digital_signature": "data:image/png;base64,iVBOR...",
  "created_at": "2024-12-13T10:30:00Z"
}
```

## 🔄 Migration History

### **Key Migrations**
1. **0001_initial**: Created CustomUser model
2. **0002_add_otp_fields**: Added OTP verification
3. **0003_nrc_application**: Created NRCApplication model
4. **0004_clean_otp_migration**: Fixed OTP field constraints
5. **0008_add_digital_signature**: Added digital signature support

## 📊 Database Statistics

### **Expected Data Volume**
- **Users**: ~10,000 citizens
- **Applications**: ~15,000 applications (1.5 per user average)
- **Files**: ~45,000 documents (3 per application)
- **Storage**: ~2GB for documents and images

### **Performance Metrics**
- **Query Response**: <100ms for standard queries
- **File Upload**: <5MB per file limit
- **Concurrent Users**: Designed for 100+ simultaneous users

---

## 🎯 Summary

The NRC System database is designed with:
- ✅ **Scalability**: Efficient indexing and relationships
- ✅ **Security**: Comprehensive authentication and authorization
- ✅ **Flexibility**: Support for multiple application types
- ✅ **Performance**: Optimized queries and file handling
- ✅ **Compliance**: Government data standards

**Total Tables**: 2 main + Django built-in tables
**Total Relationships**: 1 primary (User → Applications)
**User Types**: 3 (Citizens, Staff, Superusers)
**Security Levels**: Multi-layered authentication and authorization