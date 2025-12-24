# Zambian NRC System - Entity Relationship Diagram & Database Schema

## 🎯 System Overview
The Zambian National Registration Card (NRC) System is a comprehensive digital platform for managing NRC applications, user authentication, notifications, and administrative oversight with duplication prevention.

## 📊 Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           ZAMBIAN NRC SYSTEM - ENTITY RELATIONSHIPS                 │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐         ┌─────────────────────────┐         ┌─────────────────────────┐
│      CustomUser         │         │    NRCApplication       │         │     Notification        │
│─────────────────────────│         │─────────────────────────│         │─────────────────────────│
│ PK: id (AutoField)      │◄────────│ FK: user_id             │────────►│ FK: user_id             │
│ username (CharField)    │    1:N  │ PK: id (AutoField)      │    1:N  │ PK: id (AutoField)      │
│ email (EmailField)      │         │ application_type        │         │ notification_type       │
│ first_name (CharField)  │         │ status (CharField)      │         │ title (CharField)       │
│ last_name (CharField)   │         │ created_at (DateTime)   │         │ message (TextField)     │
│ phone_number (CharField)│         │ updated_at (DateTime)   │         │ is_read (BooleanField)  │
│ nrc_number (CharField)  │         │                         │         │ is_admin_notification   │
│ profile_image (Image)   │         │ # Applicant Details     │         │ created_at (DateTime)   │
│ bio (TextField)         │         │ village (CharField)     │         │ FK: application_id      │
│ is_staff (BooleanField) │         │ district (CharField)    │         │─────────────────────────│
│ is_superuser (Boolean)  │         │ date_of_birth (Date)    │         │                         │
│ date_joined (DateTime)  │         │ place_of_birth          │         │                         │
│ last_login (DateTime)   │         │ chief_name (CharField)  │         │                         │
│                         │         │ sex (CharField)         │         │                         │
│ # OTP Fields            │         │ photo (ImageField)      │         │                         │
│ otp_code (CharField)    │         │                         │         │                         │
│ otp_created_at          │         │ # Mother's Details      │         │                         │
│ otp_verified (Boolean)  │         │ mother_full_name        │         │                         │
│─────────────────────────│         │ mother_village          │         │                         │
│                         │         │ mother_district         │         │                         │
│                         │         │ mother_date_of_birth    │         │                         │
│                         │         │ mother_place_of_birth   │         │                         │
│                         │         │ mother_chief_name       │         │                         │
│                         │         │                         │         │                         │
│                         │         │ # Father's Details      │         │                         │
│                         │         │ father_full_name        │         │                         │
│                         │         │ father_village          │         │                         │
│                         │         │ father_district         │         │                         │
│                         │         │ father_date_of_birth    │         │                         │
│                         │         │ father_place_of_birth   │         │                         │
│                         │         │ father_chief_name       │         │                         │
│                         │         │                         │         │                         │
│                         │         │ # Documents             │         │                         │
│                         │         │ birth_certificate       │         │                         │
│                         │         │ under_five_card         │         │                         │
│                         │         │ old_nrc (FileField)     │         │                         │
│                         │         │                         │         │                         │
│                         │         │ # Generated NRC         │         │                         │
│                         │         │ nrc_number (CharField)  │         │                         │
│                         │         │ nrc_front_image         │         │                         │
│                         │         │ nrc_back_image          │         │                         │
│                         │         │ nrc_generated_at        │         │                         │
│                         │         │ digital_signature       │         │                         │
│                         │         │                         │         │                         │
│                         │         │ # Admin Fields          │         │                         │
│                         │         │ admin_notes (TextField) │         │                         │
│                         │         │ replacement_reason      │         │                         │
│                         │         │─────────────────────────│         │                         │
└─────────────────────────┘         └─────────────────────────┘         └─────────────────────────┘
            │                                       │                                       ▲
            │                                       │                                       │
            │ 1:N                                   │ 1:N                                   │ N:1
            ▼                                       ▼                                       │
┌─────────────────────────┐         ┌─────────────────────────┐                           │
│    DuplicationLog       │         │    Django Built-ins     │                           │
│─────────────────────────│         │─────────────────────────│                           │
│ PK: id (AutoField)      │         │ • User Groups           │                           │
│ FK: user_id             │         │ • User Permissions      │                           │
│ FK: admin_user_id       │         │ • Sessions              │                           │
│ detected_at (DateTime)  │         │ • Admin Log Entries     │                           │
│ detection_type          │         │ • Content Types         │                           │
│ action_taken            │         │ • Sites Framework       │                           │
│ attempted_application   │         │ • AllAuth Social        │                           │
│ matching_application_ids│         │   - Social Accounts     │                           │
│ similarity_scores       │         │   - Social Apps         │                           │
│ admin_notes (TextField) │         │   - Social Tokens       │                           │
│ ip_address (GenericIP)  │         │─────────────────────────│                           │
│ user_agent (TextField)  │         └─────────────────────────┘                           │
│─────────────────────────│                                                               │
└─────────────────────────┘                                                               │
                                                                                          │
                                                                                          │
                                    ┌─────────────────────────┐                           │
                                    │   Notification Types    │───────────────────────────┘
                                    │─────────────────────────│
                                    │ • application_approved  │
                                    │ • application_rejected  │
                                    │ • nrc_ready            │
                                    │ • new_application_sub  │
                                    │ • system_update        │
                                    │─────────────────────────│
                                    └─────────────────────────┘
```

## 🗃️ Detailed Entity Specifications

### 1. **CustomUser** (Extended Django User)
```python
# Primary Entity: User Management & Authentication
- Inherits from: AbstractUser
- Purpose: Manages user accounts, authentication, and OTP verification
- Key Features: Profile management, OTP system, admin permissions

Fields:
├── Core Identity
│   ├── id (PK, AutoField)
│   ├── username (CharField, unique)
│   ├── email (EmailField, unique)
│   ├── first_name (CharField)
│   ├── last_name (CharField)
│   └── password (CharField, hashed)
│
├── Extended Profile
│   ├── phone_number (CharField, max_length=15)
│   ├── nrc_number (CharField, max_length=20, unique)
│   ├── profile_image (ImageField)
│   └── bio (TextField, max_length=500)
│
├── Authentication & Permissions
│   ├── is_staff (BooleanField)
│   ├── is_superuser (BooleanField)
│   ├── is_active (BooleanField)
│   ├── date_joined (DateTimeField)
│   └── last_login (DateTimeField)
│
└── OTP System
    ├── otp_code (CharField, max_length=6)
    ├── otp_created_at (DateTimeField)
    └── otp_verified (BooleanField)

Relationships:
├── 1:N → NRCApplication (user can have multiple applications)
├── 1:N → Notification (user can receive multiple notifications)
└── 1:N → DuplicationLog (user can have multiple duplication logs)
```

### 2. **NRCApplication** (Core Business Entity)
```python
# Primary Entity: NRC Application Management
- Purpose: Stores all NRC application data and processing status
- Key Features: Complete applicant data, document storage, NRC generation

Fields:
├── Application Metadata
│   ├── id (PK, AutoField)
│   ├── user_id (FK → CustomUser)
│   ├── application_type (CharField: 'new'|'replacement')
│   ├── status (CharField: 'pending'|'approved'|'rejected')
│   ├── created_at (DateTimeField)
│   └── updated_at (DateTimeField)
│
├── Applicant Personal Details
│   ├── village (CharField, max_length=100)
│   ├── district (CharField, max_length=100)
│   ├── date_of_birth (DateField)
│   ├── place_of_birth (CharField, max_length=100)
│   ├── chief_name (CharField, max_length=100)
│   ├── sex (CharField: 'M'|'F')
│   └── photo (ImageField)
│
├── Mother's Information
│   ├── mother_full_name (CharField, max_length=200)
│   ├── mother_village (CharField, max_length=100)
│   ├── mother_district (CharField, max_length=100)
│   ├── mother_date_of_birth (DateField)
│   ├── mother_place_of_birth (CharField, max_length=100)
│   └── mother_chief_name (CharField, max_length=100)
│
├── Father's Information
│   ├── father_full_name (CharField, max_length=200)
│   ├── father_village (CharField, max_length=100)
│   ├── father_district (CharField, max_length=100)
│   ├── father_date_of_birth (DateField)
│   ├── father_place_of_birth (CharField, max_length=100)
│   └── father_chief_name (CharField, max_length=100)
│
├── Document Storage
│   ├── birth_certificate (FileField)
│   ├── under_five_card (FileField)
│   └── old_nrc (FileField, nullable for new applications)
│
├── Generated NRC Data
│   ├── nrc_number (CharField, max_length=20, unique)
│   ├── nrc_front_image (CharField, max_length=255)
│   ├── nrc_back_image (CharField, max_length=255)
│   ├── nrc_generated_at (DateTimeField)
│   └── digital_signature (TextField, Base64 encoded)
│
└── Administrative
    ├── admin_notes (TextField)
    └── replacement_reason (TextField)

Relationships:
├── N:1 → CustomUser (many applications belong to one user)
├── 1:N → Notification (one application can generate multiple notifications)
└── Referenced by → DuplicationLog (for duplicate detection)
```

### 3. **Notification** (Communication System)
```python
# Entity: User Communication & Alerts
- Purpose: Manages all system notifications and alerts
- Key Features: User notifications, admin alerts, application status updates

Fields:
├── Core Notification
│   ├── id (PK, AutoField)
│   ├── user_id (FK → CustomUser)
│   ├── notification_type (CharField, choices)
│   ├── title (CharField, max_length=200)
│   ├── message (TextField)
│   └── created_at (DateTimeField)
│
├── Status & Targeting
│   ├── is_read (BooleanField, default=False)
│   ├── is_admin_notification (BooleanField, default=False)
│   └── application_id (FK → NRCApplication, nullable)

Notification Types:
├── 'application_approved' → User notification when application approved
├── 'application_rejected' → User notification when application rejected
├── 'nrc_ready' → User notification when NRC card is ready
├── 'new_application_submitted' → Admin notification for new applications
└── 'system_update' → General system notifications

Relationships:
├── N:1 → CustomUser (many notifications belong to one user)
└── N:1 → NRCApplication (many notifications can reference one application)
```

### 4. **DuplicationLog** (Security & Audit)
```python
# Entity: Duplication Detection & Audit Trail
- Purpose: Logs all duplicate detection attempts and admin actions
- Key Features: Audit trail, security monitoring, duplicate prevention

Fields:
├── Detection Metadata
│   ├── id (PK, AutoField)
│   ├── user_id (FK → CustomUser)
│   ├── admin_user_id (FK → CustomUser, nullable)
│   ├── detected_at (DateTimeField)
│   └── detection_type (CharField, choices)
│
├── Detection Results
│   ├── action_taken (CharField, choices)
│   ├── attempted_application_data (JSONField)
│   ├── matching_application_ids (JSONField)
│   └── similarity_scores (JSONField)
│
├── Administrative
│   └── admin_notes (TextField)
│
└── System Information
    ├── ip_address (GenericIPAddressField)
    └── user_agent (TextField)

Detection Types:
├── 'exact_match' → 100% identical application data
├── 'similar_match' → High similarity (>95%) application data
├── 'user_existing_nrc' → User already has approved NRC
└── 'nrc_number_duplicate' → NRC number already exists

Action Types:
├── 'blocked' → Application automatically blocked
├── 'warned' → Warning issued to admin
└── 'approved_override' → Admin approved despite warning

Relationships:
├── N:1 → CustomUser (user who attempted duplicate)
└── N:1 → CustomUser (admin who handled the case)
```

## 🔗 Relationship Details

### **1:N Relationships**

#### **CustomUser → NRCApplication**
```sql
-- One user can have multiple NRC applications
-- Foreign Key: NRCApplication.user_id → CustomUser.id
-- Cascade: ON DELETE CASCADE (if user deleted, applications deleted)
-- Business Rule: Users can have multiple applications (new + replacements)
```

#### **CustomUser → Notification**
```sql
-- One user can receive multiple notifications
-- Foreign Key: Notification.user_id → CustomUser.id
-- Cascade: ON DELETE CASCADE (if user deleted, notifications deleted)
-- Business Rule: Both regular users and admins receive notifications
```

#### **CustomUser → DuplicationLog**
```sql
-- One user can have multiple duplication logs
-- Foreign Key: DuplicationLog.user_id → CustomUser.id
-- Cascade: ON DELETE CASCADE (if user deleted, logs deleted)
-- Additional: DuplicationLog.admin_user_id → CustomUser.id (SET NULL)
```

#### **NRCApplication → Notification**
```sql
-- One application can generate multiple notifications
-- Foreign Key: Notification.application_id → NRCApplication.id
-- Cascade: ON DELETE CASCADE (if application deleted, notifications deleted)
-- Business Rule: Applications generate notifications for status changes
```

### **Unique Constraints**
```sql
-- Prevent duplicate NRC numbers
ALTER TABLE CustomUser ADD CONSTRAINT unique_nrc_number UNIQUE (nrc_number);
ALTER TABLE NRCApplication ADD CONSTRAINT unique_generated_nrc UNIQUE (nrc_number);

-- Ensure unique usernames and emails
ALTER TABLE CustomUser ADD CONSTRAINT unique_username UNIQUE (username);
ALTER TABLE CustomUser ADD CONSTRAINT unique_email UNIQUE (email);
```

## 📋 Business Rules & Constraints

### **Application Rules**
1. **One Active NRC per User**: Users can only have one approved 'new' NRC application
2. **Replacement Requirements**: Replacement applications require existing approved NRC
3. **Document Requirements**: Birth certificate and under-five card mandatory for all applications
4. **Status Workflow**: pending → approved/rejected (no reverse transitions)

### **Notification Rules**
1. **Admin Notifications**: Only staff/superuser accounts receive admin notifications
2. **User Notifications**: Users only receive notifications about their own applications
3. **Automatic Creation**: Notifications automatically created on status changes
4. **Retention**: Notifications preserved for audit trail

### **Duplication Prevention**
1. **Exact Match Detection**: 100% identical personal data triggers automatic block
2. **Similarity Detection**: >95% similar data triggers admin warning
3. **NRC Number Uniqueness**: Generated NRC numbers must be globally unique
4. **Admin Override**: Admins can approve applications despite duplication warnings

### **Security Rules**
1. **OTP Expiration**: OTP codes expire after 10 minutes
2. **File Upload Security**: Document uploads restricted to specific file types
3. **Admin Access**: Admin functions require is_staff=True or is_superuser=True
4. **Audit Trail**: All duplication attempts logged with IP and user agent

## 🗂️ Database Indexes & Performance

### **Recommended Indexes**
```sql
-- User lookups
CREATE INDEX idx_customuser_username ON accounts_customuser(username);
CREATE INDEX idx_customuser_email ON accounts_customuser(email);
CREATE INDEX idx_customuser_nrc_number ON accounts_customuser(nrc_number);

-- Application queries
CREATE INDEX idx_nrcapplication_user_id ON applications_nrcapplication(user_id);
CREATE INDEX idx_nrcapplication_status ON applications_nrcapplication(status);
CREATE INDEX idx_nrcapplication_created_at ON applications_nrcapplication(created_at);
CREATE INDEX idx_nrcapplication_nrc_number ON applications_nrcapplication(nrc_number);

-- Notification queries
CREATE INDEX idx_notification_user_id ON applications_notification(user_id);
CREATE INDEX idx_notification_is_read ON applications_notification(is_read);
CREATE INDEX idx_notification_is_admin ON applications_notification(is_admin_notification);
CREATE INDEX idx_notification_created_at ON applications_notification(created_at);

-- Duplication log queries
CREATE INDEX idx_duplicationlog_user_id ON applications_duplicationlog(user_id);
CREATE INDEX idx_duplicationlog_detected_at ON applications_duplicationlog(detected_at);
CREATE INDEX idx_duplicationlog_detection_type ON applications_duplicationlog(detection_type);
```

## 📊 Data Flow Diagrams

### **Application Submission Flow**
```
User Registration → OTP Verification → Login → Application Form → 
Document Upload → Duplication Check → Admin Review → 
NRC Generation → User Notification → NRC Download
```

### **Notification Flow**
```
Application Event → NotificationService → Create Notification → 
Database Storage → Template Display → User Action → Mark as Read
```

### **Duplication Detection Flow**
```
Application Submission → Extract Personal Data → Compare with Existing → 
Calculate Similarity → Log Attempt → Admin Warning/Block → 
Admin Decision → Update Log → Continue/Stop Process
```

## 🔧 Technical Implementation Notes

### **Django Model Relationships**
- **ForeignKey**: Used for N:1 relationships with CASCADE deletion
- **OneToOneField**: Not used (no 1:1 relationships in current schema)
- **ManyToManyField**: Not used (no M:N relationships in current schema)

### **Field Types & Validation**
- **CharField**: Text fields with max_length constraints
- **TextField**: Unlimited text (notes, messages, JSON data)
- **DateTimeField**: Timestamps with timezone support
- **BooleanField**: Status flags and permissions
- **FileField/ImageField**: Document and photo storage
- **JSONField**: Flexible data storage for duplication logs

### **Custom Methods & Properties**
- **CustomUser.generate_otp()**: Creates 6-digit OTP with expiration
- **CustomUser.verify_otp()**: Validates OTP code and timing
- **CustomUser.get_initials()**: Returns user initials for avatars
- **NRCApplication.__str__()**: Human-readable representation
- **Notification.__str__()**: Notification summary

---

## 📈 System Statistics

### **Current Database State**
- **Users**: 6+ registered users (3 admins, 3+ regular users)
- **Applications**: 5 NRC applications (various statuses)
- **Notifications**: 10+ notifications (user and admin types)
- **Duplication Logs**: Audit trail of duplicate detection attempts

### **Performance Metrics**
- **Query Optimization**: Indexed fields for fast lookups
- **Storage Efficiency**: Normalized data structure
- **Scalability**: Designed for thousands of users and applications
- **Security**: Comprehensive audit trail and duplication prevention

---

**Status**: ✅ **COMPLETE AND DOCUMENTED**
**Last Updated**: December 17, 2025
**Version**: 2.0.0