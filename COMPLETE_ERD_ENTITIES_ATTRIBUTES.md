# Zambian National Registration Management System - Complete ERD Entities & Attributes

## 🎯 System Overview
**Zambian National Registration Card (NRC) Management System** - A comprehensive digital platform for managing NRC applications, user authentication, notifications, and administrative oversight with duplication prevention.

## 📊 Complete Entity List with Attributes

### 1. **CustomUser** (Primary User Entity)
```
Entity: CustomUser
Table: accounts_customuser
Purpose: User management, authentication, and profile data

Primary Key: id (BigAutoField)

Core Identity Attributes:
├── username (CharField, 150, UNIQUE, NOT NULL)
├── email (EmailField, 254, NOT NULL)
├── first_name (CharField, 150)
├── last_name (CharField, 150)
└── password (CharField, 128, hashed)

Extended Profile Attributes:
├── phone_number (CharField, 15)
├── nrc_number (CharField, 20, UNIQUE)
├── profile_image (ImageField)
└── bio (TextField, 500)

Authentication & Permission Attributes:
├── is_staff (BooleanField, default=False)
├── is_superuser (BooleanField, default=False)
├── is_active (BooleanField, default=True)
├── date_joined (DateTimeField)
└── last_login (DateTimeField)

OTP System Attributes:
├── otp_code (CharField, 6)
├── otp_created_at (DateTimeField)
└── otp_verified (BooleanField, default=False)

Relationships:
├── 1:N → NRCApplication (user)
├── 1:N → Notification (user)
├── 1:N → DuplicationLog (user)
└── 1:N → DuplicationLog (admin_user)
```

### 2. **NRCApplication** (Core Business Entity)
```
Entity: NRCApplication
Table: applications_nrcapplication
Purpose: NRC application processing and data storage

Primary Key: id (BigAutoField)
Foreign Key: user_id → CustomUser (CASCADE)

Application Metadata Attributes:
├── application_type (CharField, 20: 'new'|'replacement')
├── status (CharField, 20: 'pending'|'approved'|'rejected')
├── created_at (DateTimeField)
└── updated_at (DateTimeField)

Applicant Personal Attributes:
├── village (CharField, 100)
├── district (CharField, 100)
├── date_of_birth (DateField)
├── place_of_birth (CharField, 100)
├── chief_name (CharField, 100)
├── sex (CharField, 10: 'M'|'F')
└── photo (ImageField)

Mother Information Attributes:
├── mother_full_name (CharField, 200)
├── mother_village (CharField, 100)
├── mother_district (CharField, 100)
├── mother_date_of_birth (DateField)
├── mother_place_of_birth (CharField, 100)
└── mother_chief_name (CharField, 100)

Father Information Attributes:
├── father_full_name (CharField, 200)
├── father_village (CharField, 100)
├── father_district (CharField, 100)
├── father_date_of_birth (DateField)
├── father_place_of_birth (CharField, 100)
└── father_chief_name (CharField, 100)

Document Storage Attributes:
├── birth_certificate (FileField, required)
├── under_five_card (FileField, required)
└── old_nrc (FileField, nullable)

Generated NRC Attributes:
├── nrc_number (CharField, 20, UNIQUE)
├── nrc_front_image (CharField, 255)
├── nrc_back_image (CharField, 255)
├── nrc_generated_at (DateTimeField)
└── digital_signature (TextField, Base64)

Administrative Attributes:
├── admin_notes (TextField)
└── replacement_reason (TextField)

Relationships:
├── N:1 → CustomUser (user)
└── 1:N → Notification (application)
```

### 3. **Notification** (Communication Entity)
```
Entity: Notification
Table: applications_notification
Purpose: User and admin notifications system

Primary Key: id (BigAutoField)
Foreign Key: user_id → CustomUser (CASCADE)
Foreign Key: application_id → NRCApplication (CASCADE, nullable)

Core Notification Attributes:
├── notification_type (CharField, 50)
│   ├── 'application_approved'
│   ├── 'application_rejected'
│   ├── 'nrc_ready'
│   ├── 'new_application_submitted'
│   └── 'system_update'
├── title (CharField, 200)
├── message (TextField)
└── created_at (DateTimeField)

Status & Targeting Attributes:
├── is_read (BooleanField, default=False)
└── is_admin_notification (BooleanField, default=False)

Relationships:
├── N:1 → CustomUser (user)
└── N:1 → NRCApplication (application)
```

### 4. **DuplicationLog** (Security & Audit Entity)
```
Entity: DuplicationLog
Table: applications_duplicationlog
Purpose: Duplicate detection audit trail and security monitoring

Primary Key: id (BigAutoField)
Foreign Key: user_id → CustomUser (CASCADE)
Foreign Key: admin_user_id → CustomUser (SET_NULL, nullable)

Detection Metadata Attributes:
├── detected_at (DateTimeField)
├── detection_type (CharField, 50)
│   ├── 'exact_match'
│   ├── 'similar_match'
│   ├── 'user_existing_nrc'
│   └── 'nrc_number_duplicate'
└── action_taken (CharField, 50)
    ├── 'blocked'
    ├── 'warned'
    └── 'approved_override'

Detection Results Attributes:
├── attempted_application_data (JSONField)
├── matching_application_ids (JSONField)
└── similarity_scores (JSONField)

Administrative Attributes:
└── admin_notes (TextField)

System Information Attributes:
├── ip_address (GenericIPAddressField)
└── user_agent (TextField)

Relationships:
├── N:1 → CustomUser (user)
└── N:1 → CustomUser (admin_user)
```

## 🔗 Entity Relationship Summary

### **Primary Relationships:**
```
CustomUser (1) ←→ (N) NRCApplication
CustomUser (1) ←→ (N) Notification
CustomUser (1) ←→ (N) DuplicationLog (as user)
CustomUser (1) ←→ (N) DuplicationLog (as admin)
NRCApplication (1) ←→ (N) Notification
```

### **Relationship Details:**
| From Entity | To Entity | Relationship | Foreign Key | On Delete | Description |
|-------------|-----------|--------------|-------------|-----------|-------------|
| CustomUser | NRCApplication | 1:N | user_id | CASCADE | User can have multiple applications |
| CustomUser | Notification | 1:N | user_id | CASCADE | User can receive multiple notifications |
| CustomUser | DuplicationLog | 1:N | user_id | CASCADE | User can have multiple duplication logs |
| CustomUser | DuplicationLog | 1:N | admin_user_id | SET_NULL | Admin can handle multiple cases |
| NRCApplication | Notification | 1:N | application_id | CASCADE | Application can generate multiple notifications |

## 📋 ERD Diagram Structure (For Visual Tools)

### **Entity Boxes:**
```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    ZAMBIAN NRC SYSTEM - ENTITY RELATIONSHIP DIAGRAM                 │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐    ┌─────────────────────────┐    ┌─────────────────────────┐
│      CustomUser         │    │    NRCApplication       │    │     Notification        │
├─────────────────────────┤    ├─────────────────────────┤    ├─────────────────────────┤
│ PK: id                  │    │ PK: id                  │    │ PK: id                  │
│ UK: username            │◄───┤ FK: user_id             │───►│ FK: user_id             │
│ UK: email               │1:N │                         │1:N │ FK: application_id      │
│ UK: nrc_number          │    │ application_type        │    │                         │
│                         │    │ status                  │    │ notification_type       │
│ # Core Identity         │    │ created_at              │    │ title                   │
│ username                │    │ updated_at              │    │ message                 │
│ email                   │    │                         │    │ is_read                 │
│ first_name              │    │ # Personal Details      │    │ is_admin_notification   │
│ last_name               │    │ village                 │    │ created_at              │
│ password                │    │ district                │    │                         │
│                         │    │ date_of_birth           │    │                         │
│ # Extended Profile      │    │ place_of_birth          │    │                         │
│ phone_number            │    │ chief_name              │    │                         │
│ nrc_number              │    │ sex                     │    │                         │
│ profile_image           │    │ photo                   │    │                         │
│ bio                     │    │                         │    │                         │
│                         │    │ # Mother Details        │    │                         │
│ # Permissions           │    │ mother_full_name        │    │                         │
│ is_staff                │    │ mother_village          │    │                         │
│ is_superuser            │    │ mother_district         │    │                         │
│ is_active               │    │ mother_date_of_birth    │    │                         │
│ date_joined             │    │ mother_place_of_birth   │    │                         │
│ last_login              │    │ mother_chief_name       │    │                         │
│                         │    │                         │    │                         │
│ # OTP System            │    │ # Father Details        │    │                         │
│ otp_code                │    │ father_full_name        │    │                         │
│ otp_created_at          │    │ father_village          │    │                         │
│ otp_verified            │    │ father_district         │    │                         │
└─────────────────────────┘    │ father_date_of_birth    │    │                         │
            │                  │ father_place_of_birth   │    │                         │
            │                  │ father_chief_name       │    │                         │
            │ 1:N              │                         │    │                         │
            ▼                  │ # Documents             │    │                         │
┌─────────────────────────┐    │ birth_certificate       │    │                         │
│    DuplicationLog       │    │ under_five_card         │    │                         │
├─────────────────────────┤    │ old_nrc                 │    │                         │
│ PK: id                  │    │                         │    │                         │
│ FK: user_id             │    │ # Generated NRC         │    │                         │
│ FK: admin_user_id       │    │ nrc_number              │    │                         │
│                         │    │ nrc_front_image         │    │                         │
│ detected_at             │    │ nrc_back_image          │    │                         │
│ detection_type          │    │ nrc_generated_at        │    │                         │
│ action_taken            │    │ digital_signature       │    │                         │
│                         │    │                         │    │                         │
│ # Detection Results     │    │ # Administrative        │    │                         │
│ attempted_application   │    │ admin_notes             │    │                         │
│ matching_application_ids│    │ replacement_reason      │    │                         │
│ similarity_scores       │    │                         │    │                         │
│                         │    │                         │    │                         │
│ # Administrative        │    │                         │    │                         │
│ admin_notes             │    │                         │    │                         │
│                         │    │                         │    │                         │
│ # System Info           │    │                         │    │                         │
│ ip_address              │    │                         │    │                         │
│ user_agent              │    │                         │    │                         │
└─────────────────────────┘    └─────────────────────────┘    └─────────────────────────┘
```

## 🎯 Key Constraints & Business Rules

### **Unique Constraints:**
- CustomUser.username (UNIQUE)
- CustomUser.email (UNIQUE) 
- CustomUser.nrc_number (UNIQUE)
- NRCApplication.nrc_number (UNIQUE)

### **Required Fields:**
- All personal information fields in NRCApplication
- Birth certificate and under-five card documents
- Mother and father complete information
- User authentication fields

### **Business Rules:**
1. One approved 'new' NRC application per user
2. Replacement applications require existing approved NRC
3. Admin users bypass OTP verification
4. Automatic notification creation on status changes
5. Comprehensive duplication prevention with audit trail

## 📊 Current System Statistics
- **Users**: 11 total (3 admins, 8 regular)
- **Applications**: 5 total (1 pending, 4 approved)
- **Notifications**: 9 total (3 unread, 3 admin)
- **Security Logs**: 0 duplication attempts

## 🛠️ ERD Creation Tools Compatibility

### **Recommended Tools:**
1. **Draw.io / Diagrams.net** - Free online ERD tool
2. **Lucidchart** - Professional diagramming
3. **MySQL Workbench** - Database-specific ERD
4. **dbdiagram.io** - Simple online database designer
5. **Visual Paradigm** - Enterprise modeling tool

### **ERD Export Format:**
```sql
-- Table Creation Order (for ERD tools):
1. CustomUser (no dependencies)
2. NRCApplication (depends on CustomUser)
3. Notification (depends on CustomUser, NRCApplication)
4. DuplicationLog (depends on CustomUser)
```

---

**Status**: ✅ **READY FOR ERD CREATION**
**Entities**: 4 core entities
**Relationships**: 5 primary relationships
**Attributes**: 50+ total attributes
**Last Updated**: December 17, 2025