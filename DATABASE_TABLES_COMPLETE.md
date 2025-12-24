# Complete Database Schema Documentation

## Overview
This document provides a comprehensive overview of all database tables in the Zambian NRC Online System, including their structure, relationships, and purposes.

## Database Architecture

### Core Applications
- **accounts**: User management and authentication
- **applications**: NRC application processing
- **Django Built-in**: Authentication, sessions, admin, etc.

---

## 1. User Management (accounts app)

### accounts_customuser
**Purpose**: Extended user model with NRC-specific fields and OTP functionality

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PRIMARY KEY | Unique user identifier |
| password | CharField(128) | NOT NULL | Hashed password |
| last_login | DateTimeField | NULL | Last login timestamp |
| is_superuser | BooleanField | DEFAULT FALSE | Django superuser flag |
| username | CharField(150) | UNIQUE, NOT NULL | Unique username |
| first_name | CharField(150) | | User's first name |
| last_name | CharField(150) | | User's last name |
| email | EmailField(254) | | Email address |
| is_staff | BooleanField | DEFAULT FALSE | Django staff flag |
| is_active | BooleanField | DEFAULT TRUE | Account active status |
| date_joined | DateTimeField | DEFAULT NOW | Account creation date |
| **phone_number** | CharField(15) | | Phone number |
| **nrc_number** | CharField(20) | UNIQUE, NULL | User's NRC number |
| **profile_image** | ImageField | NULL | Profile picture |
| **bio** | TextField(500) | | User biography |
| **is_officer** | BooleanField | DEFAULT FALSE | NRC officer designation |
| **otp_code** | CharField(6) | NULL | Temporary OTP code |
| **otp_created_at** | DateTimeField | NULL | OTP generation time |
| **otp_verified** | BooleanField | DEFAULT FALSE | OTP verification status |

**Indexes**: username, email, nrc_number (unique)

---

## 2. NRC Applications (applications app)

### applications_nrcapplication (Legacy - Unified Model)
**Purpose**: Main table for all NRC applications (new and replacement)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PRIMARY KEY | Application ID |
| **user_id** | ForeignKey | NOT NULL | Reference to CustomUser |
| **application_type** | CharField(20) | NOT NULL | 'new' or 'replacement' |
| **status** | CharField(20) | DEFAULT 'pending' | Application status |
| created_at | DateTimeField | DEFAULT NOW | Application submission |
| updated_at | DateTimeField | AUTO NOW | Last modification |
| **village** | CharField(100) | NOT NULL | Applicant's village |
| **district** | CharField(100) | DEFAULT 'Not provided' | Applicant's district |
| **date_of_birth** | DateField | NOT NULL | Applicant's DOB |
| **place_of_birth** | CharField(100) | NOT NULL | Birth location |
| **chief_name** | CharField(100) | NOT NULL | Traditional leader |
| **sex** | CharField(10) | DEFAULT 'M' | Gender (M/F) |
| **photo** | ImageField | NULL | Passport photo |
| **collection_province** | CharField(100) | NULL | Collection province |
| **collection_station** | CharField(200) | NULL | Collection office |
| **mother_full_name** | CharField(200) | DEFAULT 'Not provided' | Mother's name |
| **mother_village** | CharField(100) | NOT NULL | Mother's village |
| **mother_district** | CharField(100) | DEFAULT 'Not provided' | Mother's district |
| **mother_date_of_birth** | DateField | NOT NULL | Mother's DOB |
| **mother_place_of_birth** | CharField(100) | NOT NULL | Mother's birth place |
| **mother_chief_name** | CharField(100) | NOT NULL | Mother's chief |
| **father_full_name** | CharField(200) | DEFAULT 'Not provided' | Father's name |
| **father_village** | CharField(100) | NOT NULL | Father's village |
| **father_district** | CharField(100) | DEFAULT 'Not provided' | Father's district |
| **father_date_of_birth** | DateField | NOT NULL | Father's DOB |
| **father_place_of_birth** | CharField(100) | NOT NULL | Father's birth place |
| **father_chief_name** | CharField(100) | NOT NULL | Father's chief |
| **birth_certificate** | FileField | NOT NULL | Birth certificate upload |
| **under_five_card** | FileField | NOT NULL | Under-5 card upload |
| **old_nrc** | FileField | NULL | Old NRC (replacements only) |
| **replacement_reason** | TextField | | Replacement reason |
| **admin_notes** | TextField | | Officer/admin notes |
| **nrc_number** | CharField(20) | UNIQUE, NULL | Generated NRC number |
| **nrc_front_image** | CharField(255) | NULL | Generated NRC front path |
| **nrc_back_image** | CharField(255) | NULL | Generated NRC back path |
| **nrc_generated_at** | DateTimeField | NULL | NRC generation timestamp |

**Indexes**: user_id, status, application_type, nrc_number (unique), created_at

### applications_newnrcapplication (New Separated Model)
**Purpose**: Dedicated table for new NRC applications

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PRIMARY KEY | Application ID |
| **user_id** | ForeignKey | NOT NULL | Reference to CustomUser |
| **status** | CharField(20) | DEFAULT 'pending' | Application status |
| created_at | DateTimeField | DEFAULT NOW | Application submission |
| updated_at | DateTimeField | AUTO NOW | Last modification |
| *[All BaseNRCApplication fields]* | | | Same as legacy model |

**Note**: Inherits all fields from BaseNRCApplication abstract model

### applications_nrcreplacement (New Separated Model)
**Purpose**: Dedicated table for NRC replacement applications

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PRIMARY KEY | Application ID |
| **user_id** | ForeignKey | NOT NULL | Reference to CustomUser |
| **status** | CharField(20) | DEFAULT 'pending' | Application status |
| created_at | DateTimeField | DEFAULT NOW | Application submission |
| updated_at | DateTimeField | AUTO NOW | Last modification |
| *[All BaseNRCApplication fields]* | | | Same as legacy model |
| **old_nrc** | FileField | NOT NULL | Old/damaged NRC upload |
| **replacement_reason** | TextField | NOT NULL | Reason for replacement |

**Note**: Inherits all fields from BaseNRCApplication + replacement-specific fields

---

## 3. Django Built-in Tables

### auth_group
**Purpose**: User groups for permissions
- id, name

### auth_group_permissions
**Purpose**: Many-to-many relationship between groups and permissions
- id, group_id, permission_id

### auth_permission
**Purpose**: System permissions
- id, name, content_type_id, codename

### django_content_type
**Purpose**: Content type framework
- id, app_label, model

### django_migrations
**Purpose**: Migration tracking
- id, app, name, applied

### django_session
**Purpose**: User sessions
- session_key, session_data, expire_date

### django_admin_log
**Purpose**: Admin action logging
- id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id

### django_site
**Purpose**: Sites framework
- id, domain, name

---

## 4. Social Authentication (allauth)

### socialaccount_socialapp
**Purpose**: OAuth application configurations
- id, provider, name, client_id, secret, key

### socialaccount_socialaccount
**Purpose**: Social media account links
- id, provider, uid, last_login, date_joined, extra_data, user_id

### socialaccount_socialtoken
**Purpose**: OAuth tokens
- id, token, token_secret, expires_at, account_id, app_id

### account_emailaddress
**Purpose**: Email address verification
- id, email, verified, primary, user_id

### account_emailconfirmation
**Purpose**: Email confirmation tokens
- id, created, sent, key, email_address_id

---

## 5. Relationships and Constraints

### Primary Relationships
```
CustomUser (1) ←→ (Many) NRCApplication
CustomUser (1) ←→ (Many) NewNRCApplication  
CustomUser (1) ←→ (Many) NRCReplacement
CustomUser (1) ←→ (Many) SocialAccount
CustomUser (1) ←→ (Many) EmailAddress
```

### Key Constraints
- **Unique Constraints**: username, email, nrc_number (users), nrc_number (applications)
- **Foreign Key Constraints**: All application tables reference CustomUser
- **Check Constraints**: Status choices, gender choices, application type choices

### Indexes for Performance
- User lookups: username, email, nrc_number
- Application queries: user_id, status, created_at, application_type
- Admin searches: nrc_number, status combinations

---

## 6. Data Migration Strategy

### Current State (Post-Migration)
1. **Legacy Model**: `applications_nrcapplication` - Contains all existing data
2. **New Models**: `applications_newnrcapplication`, `applications_nrcreplacement` - Ready for new data
3. **Migration Path**: Data can be migrated from legacy to new models when ready

### Migration Benefits
- **Separation of Concerns**: Different application types in separate tables
- **Optimized Queries**: Type-specific queries are faster
- **Cleaner Code**: Type-specific business logic
- **Future Extensibility**: Easy to add type-specific fields

---

## 7. File Storage Structure

### Media Files Organization
```
media/
├── photos/
│   └── applicants/          # User passport photos
├── documents/
│   ├── birth_certificates/  # Birth certificate uploads
│   ├── under_five_cards/    # Under-5 card uploads
│   └── old_nrc/            # Old NRC documents (replacements)
├── profile_images/          # User profile pictures
└── generated_nrc/          # Generated NRC card images
    ├── front/
    └── back/
```

### File Field Mappings
- **photo**: `photos/applicants/`
- **birth_certificate**: `documents/birth_certificates/`
- **under_five_card**: `documents/under_five_cards/`
- **old_nrc**: `documents/old_nrc/`
- **profile_image**: `profile_images/`
- **nrc_front_image**: Path stored as string (generated files)
- **nrc_back_image**: Path stored as string (generated files)

---

## 8. Security Considerations

### Data Protection
- **Password Hashing**: Django's built-in PBKDF2 algorithm
- **File Upload Validation**: Type and size restrictions
- **OTP Security**: 10-minute expiration, single-use codes
- **Session Security**: Secure session management

### Access Control
- **User Levels**: Regular users, Officers (is_officer=True), Staff, Superusers
- **Permission System**: Django's built-in permissions + custom officer checks
- **Data Isolation**: Users can only access their own applications

### Audit Trail
- **Timestamps**: created_at, updated_at on all applications
- **Admin Logging**: Django admin logs all administrative actions
- **Status Tracking**: Application status changes are logged

---

## 9. Performance Optimizations

### Database Indexes
```sql
-- User lookups
CREATE INDEX idx_customuser_username ON accounts_customuser(username);
CREATE INDEX idx_customuser_nrc_number ON accounts_customuser(nrc_number);

-- Application queries
CREATE INDEX idx_nrcapp_user_status ON applications_nrcapplication(user_id, status);
CREATE INDEX idx_nrcapp_created_at ON applications_nrcapplication(created_at);
CREATE INDEX idx_nrcapp_type_status ON applications_nrcapplication(application_type, status);
```

### Query Optimizations
- **select_related()**: Used for user joins in application queries
- **Pagination**: Implemented on all list views
- **Filtering**: Efficient status and type filtering

---

## 10. Backup and Recovery

### Critical Data
1. **User Accounts**: All user information and credentials
2. **Applications**: All NRC application data and documents
3. **Generated NRCs**: Issued NRC numbers and card images
4. **Audit Logs**: Administrative actions and changes

### Backup Strategy
- **Database Dumps**: Regular PostgreSQL/SQLite backups
- **Media Files**: File system backups of uploaded documents
- **Configuration**: Environment variables and settings backup

---

This schema supports the complete NRC application lifecycle from user registration through application submission, processing, approval, and NRC card generation, with full audit trails and security measures.