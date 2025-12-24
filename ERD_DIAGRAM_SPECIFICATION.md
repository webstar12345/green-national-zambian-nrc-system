# ERD Diagram Specification - Zambian NRC Management System

## 🎯 Quick Reference for ERD Creation

### **System Name:** Zambian National Registration Card Management System
### **Total Entities:** 4
### **Total Relationships:** 5

---

## 📊 Entity Specifications (Simplified for ERD Tools)

### **Entity 1: CustomUser**
```
Table Name: accounts_customuser
Primary Key: id (BigAutoField)

Attributes:
- id (PK, BigAutoField)
- username (VARCHAR(150), UNIQUE, NOT NULL)
- email (VARCHAR(254), NOT NULL)
- first_name (VARCHAR(150))
- last_name (VARCHAR(150))
- password (VARCHAR(128), NOT NULL)
- phone_number (VARCHAR(15))
- nrc_number (VARCHAR(20), UNIQUE)
- profile_image (VARCHAR(100))
- bio (TEXT)
- is_staff (BOOLEAN, DEFAULT FALSE)
- is_superuser (BOOLEAN, DEFAULT FALSE)
- is_active (BOOLEAN, DEFAULT TRUE)
- date_joined (DATETIME, NOT NULL)
- last_login (DATETIME)
- otp_code (VARCHAR(6))
- otp_created_at (DATETIME)
- otp_verified (BOOLEAN, DEFAULT FALSE)
```

### **Entity 2: NRCApplication**
```
Table Name: applications_nrcapplication
Primary Key: id (BigAutoField)
Foreign Key: user_id → CustomUser.id

Attributes:
- id (PK, BigAutoField)
- user_id (FK, BigAutoField, NOT NULL)
- application_type (VARCHAR(20), NOT NULL)
- status (VARCHAR(20), DEFAULT 'pending')
- created_at (DATETIME, NOT NULL)
- updated_at (DATETIME, NOT NULL)
- village (VARCHAR(100), NOT NULL)
- district (VARCHAR(100), NOT NULL)
- date_of_birth (DATE, NOT NULL)
- place_of_birth (VARCHAR(100), NOT NULL)
- chief_name (VARCHAR(100), NOT NULL)
- sex (VARCHAR(10), NOT NULL)
- photo (VARCHAR(100))
- mother_full_name (VARCHAR(200), NOT NULL)
- mother_village (VARCHAR(100), NOT NULL)
- mother_district (VARCHAR(100), NOT NULL)
- mother_date_of_birth (DATE, NOT NULL)
- mother_place_of_birth (VARCHAR(100), NOT NULL)
- mother_chief_name (VARCHAR(100), NOT NULL)
- father_full_name (VARCHAR(200), NOT NULL)
- father_village (VARCHAR(100), NOT NULL)
- father_district (VARCHAR(100), NOT NULL)
- father_date_of_birth (DATE, NOT NULL)
- father_place_of_birth (VARCHAR(100), NOT NULL)
- father_chief_name (VARCHAR(100), NOT NULL)
- birth_certificate (VARCHAR(100), NOT NULL)
- under_five_card (VARCHAR(100), NOT NULL)
- old_nrc (VARCHAR(100))
- nrc_number (VARCHAR(20), UNIQUE)
- nrc_front_image (VARCHAR(255))
- nrc_back_image (VARCHAR(255))
- nrc_generated_at (DATETIME)
- digital_signature (TEXT)
- admin_notes (TEXT)
- replacement_reason (TEXT)
```

### **Entity 3: Notification**
```
Table Name: applications_notification
Primary Key: id (BigAutoField)
Foreign Key: user_id → CustomUser.id
Foreign Key: application_id → NRCApplication.id

Attributes:
- id (PK, BigAutoField)
- user_id (FK, BigAutoField, NOT NULL)
- application_id (FK, BigAutoField)
- notification_type (VARCHAR(50), NOT NULL)
- title (VARCHAR(200), NOT NULL)
- message (TEXT, NOT NULL)
- is_read (BOOLEAN, DEFAULT FALSE)
- is_admin_notification (BOOLEAN, DEFAULT FALSE)
- created_at (DATETIME, NOT NULL)
```

### **Entity 4: DuplicationLog**
```
Table Name: applications_duplicationlog
Primary Key: id (BigAutoField)
Foreign Key: user_id → CustomUser.id
Foreign Key: admin_user_id → CustomUser.id

Attributes:
- id (PK, BigAutoField)
- user_id (FK, BigAutoField, NOT NULL)
- admin_user_id (FK, BigAutoField)
- detected_at (DATETIME, NOT NULL)
- detection_type (VARCHAR(50), NOT NULL)
- action_taken (VARCHAR(50), NOT NULL)
- attempted_application_data (JSON, NOT NULL)
- matching_application_ids (JSON, NOT NULL)
- similarity_scores (JSON, NOT NULL)
- admin_notes (TEXT)
- ip_address (VARCHAR(39))
- user_agent (TEXT)
```

---

## 🔗 Relationship Specifications

### **Relationship 1: User to Applications**
```
From: CustomUser
To: NRCApplication
Type: One-to-Many (1:N)
Foreign Key: NRCApplication.user_id → CustomUser.id
On Delete: CASCADE
Description: One user can have multiple NRC applications
```

### **Relationship 2: User to Notifications**
```
From: CustomUser
To: Notification
Type: One-to-Many (1:N)
Foreign Key: Notification.user_id → CustomUser.id
On Delete: CASCADE
Description: One user can receive multiple notifications
```

### **Relationship 3: Application to Notifications**
```
From: NRCApplication
To: Notification
Type: One-to-Many (1:N)
Foreign Key: Notification.application_id → NRCApplication.id
On Delete: CASCADE
Description: One application can generate multiple notifications
```

### **Relationship 4: User to Duplication Logs (as User)**
```
From: CustomUser
To: DuplicationLog
Type: One-to-Many (1:N)
Foreign Key: DuplicationLog.user_id → CustomUser.id
On Delete: CASCADE
Description: One user can have multiple duplication detection logs
```

### **Relationship 5: User to Duplication Logs (as Admin)**
```
From: CustomUser
To: DuplicationLog
Type: One-to-Many (1:N)
Foreign Key: DuplicationLog.admin_user_id → CustomUser.id
On Delete: SET NULL
Description: One admin can handle multiple duplication cases
```

---

## 📋 ERD Creation Instructions

### **Step 1: Create Entities**
1. Create 4 entity boxes with names: CustomUser, NRCApplication, Notification, DuplicationLog
2. Add all attributes listed above to each entity
3. Mark Primary Keys (PK) and Foreign Keys (FK)
4. Mark UNIQUE constraints on username, email, nrc_number fields

### **Step 2: Add Relationships**
1. Draw line from CustomUser to NRCApplication (1:N)
2. Draw line from CustomUser to Notification (1:N)
3. Draw line from NRCApplication to Notification (1:N)
4. Draw line from CustomUser to DuplicationLog (1:N) - user relationship
5. Draw line from CustomUser to DuplicationLog (1:N) - admin relationship

### **Step 3: Add Relationship Labels**
- Label each relationship line with cardinality (1:N)
- Add foreign key field names
- Mark cascade/set null behaviors

### **Step 4: Visual Formatting**
- Use different colors for different entity types
- Highlight primary keys in bold
- Use dotted lines for optional relationships
- Add entity descriptions/purposes

---

## 🎨 Visual ERD Layout Suggestion

```
Layout Recommendation:

┌─────────────────┐
│   CustomUser    │ (Top Center - Main Entity)
└─────────────────┘
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
┌─────┐ ┌─────┐ ┌─────┐
│ NRC │ │Notif│ │Dupl │ (Second Row - Related Entities)
│App  │ │     │ │Log  │
└─────┘ └─────┘ └─────┘
    │       ▲
    └───────┘ (NRCApplication to Notification)
```

---

## 🛠️ Tool-Specific Instructions

### **For Draw.io/Diagrams.net:**
1. Use "Entity Relationship" template
2. Drag entity shapes for each table
3. Add attributes using text boxes
4. Use connector lines for relationships
5. Export as PNG/PDF for documentation

### **For dbdiagram.io:**
```sql
// Copy-paste this code into dbdiagram.io:

Table CustomUser {
  id bigint [pk, increment]
  username varchar(150) [unique, not null]
  email varchar(254) [not null]
  first_name varchar(150)
  last_name varchar(150)
  password varchar(128) [not null]
  phone_number varchar(15)
  nrc_number varchar(20) [unique]
  profile_image varchar(100)
  bio text
  is_staff boolean [default: false]
  is_superuser boolean [default: false]
  is_active boolean [default: true]
  date_joined datetime [not null]
  last_login datetime
  otp_code varchar(6)
  otp_created_at datetime
  otp_verified boolean [default: false]
}

Table NRCApplication {
  id bigint [pk, increment]
  user_id bigint [ref: > CustomUser.id, not null]
  application_type varchar(20) [not null]
  status varchar(20) [default: 'pending']
  created_at datetime [not null]
  updated_at datetime [not null]
  village varchar(100) [not null]
  district varchar(100) [not null]
  date_of_birth date [not null]
  place_of_birth varchar(100) [not null]
  chief_name varchar(100) [not null]
  sex varchar(10) [not null]
  photo varchar(100)
  mother_full_name varchar(200) [not null]
  mother_village varchar(100) [not null]
  mother_district varchar(100) [not null]
  mother_date_of_birth date [not null]
  mother_place_of_birth varchar(100) [not null]
  mother_chief_name varchar(100) [not null]
  father_full_name varchar(200) [not null]
  father_village varchar(100) [not null]
  father_district varchar(100) [not null]
  father_date_of_birth date [not null]
  father_place_of_birth varchar(100) [not null]
  father_chief_name varchar(100) [not null]
  birth_certificate varchar(100) [not null]
  under_five_card varchar(100) [not null]
  old_nrc varchar(100)
  nrc_number varchar(20) [unique]
  nrc_front_image varchar(255)
  nrc_back_image varchar(255)
  nrc_generated_at datetime
  digital_signature text
  admin_notes text
  replacement_reason text
}

Table Notification {
  id bigint [pk, increment]
  user_id bigint [ref: > CustomUser.id, not null]
  application_id bigint [ref: > NRCApplication.id]
  notification_type varchar(50) [not null]
  title varchar(200) [not null]
  message text [not null]
  is_read boolean [default: false]
  is_admin_notification boolean [default: false]
  created_at datetime [not null]
}

Table DuplicationLog {
  id bigint [pk, increment]
  user_id bigint [ref: > CustomUser.id, not null]
  admin_user_id bigint [ref: > CustomUser.id]
  detected_at datetime [not null]
  detection_type varchar(50) [not null]
  action_taken varchar(50) [not null]
  attempted_application_data json [not null]
  matching_application_ids json [not null]
  similarity_scores json [not null]
  admin_notes text
  ip_address varchar(39)
  user_agent text
}
```

### **For MySQL Workbench:**
1. Create new EER Model
2. Add tables using Table Editor
3. Define all columns with data types
4. Create relationships using Relationship Editor
5. Generate forward engineer script

---

**Status**: ✅ **READY FOR ERD CREATION**
**Format**: Compatible with all major ERD tools
**Complexity**: 4 entities, 5 relationships, 50+ attributes
**Last Updated**: December 17, 2025