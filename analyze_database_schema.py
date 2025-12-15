#!/usr/bin/env python
"""
Analyze Database Schema - Complete NRC System Analysis
Display all tables, relationships, and user types in the NRC system
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.db import connection
from django.apps import apps
from django.contrib.auth import get_user_model
from applications.models import NRCApplication

User = get_user_model()

def analyze_database_schema():
    """Display comprehensive database schema information"""
    print("🗄️  NRC SYSTEM DATABASE SCHEMA - COMPLETE ANALYSIS")
    print("=" * 70)
    
    # Database info
    db_settings = connection.settings_dict
    print(f"\n📊 Database Information:")
    print(f"   Name: {db_settings.get('NAME', 'SQLite')}")
    print(f"   Engine: {db_settings['ENGINE'].split('.')[-1]}")
    print(f"   Host: {db_settings.get('HOST', 'localhost')}")
    
    # Get all models
    models = apps.get_models()
    print(f"\n📋 Total Models: {len(models)}")
    
    # Focus on main models
    main_models = [User, NRCApplication]
    
    print(f"\n🏗️  MAIN SYSTEM MODELS")
    print("-" * 40)
    
    for model in main_models:
        show_model_details(model)
    
    # Show relationships
    print(f"\n🔗 RELATIONSHIPS & CONSTRAINTS")
    print("-" * 40)
    show_relationships()
    
    # Show user types
    print(f"\n👥 USER TYPES & PERMISSIONS")
    print("-" * 40)
    show_user_types()
    
    # Show statistics
    print(f"\n📈 DATABASE STATISTICS")
    print("-" * 40)
    show_statistics()

def show_model_details(model):
    """Show detailed information about a model"""
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    table_name = model._meta.db_table
    
    print(f"\n🏷️  {app_label}.{model_name.upper()}")
    print(f"   📋 Table: {table_name}")
    
    # Show fields with detailed info
    fields = model._meta.get_fields()
    print(f"   📝 Fields ({len(fields)}):")
    
    for field in fields:
        show_field_details(field)

def show_field_details(field):
    """Show detailed field information"""
    field_type = field.__class__.__name__
    
    # Build field info string
    if hasattr(field, 'max_length') and field.max_length:
        field_info = f"{field_type}({field.max_length})"
    elif field_type == 'TextField':
        field_info = f"{field_type}(unlimited)"
    else:
        field_info = field_type
    
    # Add constraints
    constraints = []
    if hasattr(field, 'primary_key') and field.primary_key:
        constraints.append("🔑 PK")
    if hasattr(field, 'unique') and field.unique:
        constraints.append("🎯 UNIQUE")
    if hasattr(field, 'null') and not field.null and not getattr(field, 'primary_key', False):
        constraints.append("❗ NOT NULL")
    if hasattr(field, 'default') and field.default is not None:
        default_val = field.default
        if callable(default_val):
            constraints.append("⏰ AUTO")
        else:
            constraints.append(f"📌 DEFAULT")
    
    constraint_str = f" [{', '.join(constraints)}]" if constraints else ""
    
    # Add description for important fields
    descriptions = {
        'user': 'Foreign key to CustomUser',
        'nrc_number': 'Generated NRC number (Z + 8 digits)',
        'digital_signature': 'Base64 encoded signature image',
        'otp_code': 'Temporary 6-digit verification code',
        'status': 'Application status (pending/approved/rejected)',
        'application_type': 'Type of application (new/replacement)'
    }
    
    description = descriptions.get(field.name, '')
    desc_str = f" - {description}" if description else ""
    
    print(f"     • {field.name}: {field_info}{constraint_str}{desc_str}")

def show_relationships():
    """Show database relationships"""
    print("   🔗 User → Applications (One-to-Many)")
    print("      CustomUser.id ←→ NRCApplication.user_id")
    print("      Constraint: CASCADE DELETE")
    print("      Business Rule: One user can have multiple applications")
    
    print("\n   📊 Relationship Details:")
    print("      • Type: Foreign Key")
    print("      • Cardinality: 1:N")
    print("      • Delete Behavior: CASCADE")
    print("      • Index: Automatic on user_id")

def show_user_types():
    """Show different user types and their permissions"""
    user_types = [
        {
            'name': 'Regular Users (Citizens)',
            'conditions': 'is_staff=False, is_superuser=False',
            'permissions': [
                '✅ Create NRC applications',
                '✅ View own applications',
                '✅ Add digital signatures',
                '✅ Download own NRC cards',
                '❌ Access admin functions'
            ]
        },
        {
            'name': 'Staff Members (Government Officers)',
            'conditions': 'is_staff=True, is_superuser=False',
            'permissions': [
                '✅ All regular user permissions',
                '✅ Access admin dashboard',
                '✅ View all applications',
                '✅ Approve/reject applications',
                '✅ Generate NRC cards',
                '✅ View reports',
                '❌ User management'
            ]
        },
        {
            'name': 'Superusers (System Administrators)',
            'conditions': 'is_staff=True, is_superuser=True',
            'permissions': [
                '✅ All staff permissions',
                '✅ User management',
                '✅ System configuration',
                '✅ Database access',
                '✅ Django admin access'
            ]
        }
    ]
    
    for user_type in user_types:
        print(f"\n   👤 {user_type['name']}")
        print(f"      Conditions: {user_type['conditions']}")
        print("      Permissions:")
        for perm in user_type['permissions']:
            print(f"        {perm}")

def show_statistics():
    """Show database statistics"""
    try:
        # Count records
        user_count = User.objects.count()
        app_count = NRCApplication.objects.count()
        pending_count = NRCApplication.objects.filter(status='pending').count()
        approved_count = NRCApplication.objects.filter(status='approved').count()
        rejected_count = NRCApplication.objects.filter(status='rejected').count()
        
        print(f"   📊 Record Counts:")
        print(f"      Users: {user_count}")
        print(f"      Applications: {app_count}")
        print(f"        • Pending: {pending_count}")
        print(f"        • Approved: {approved_count}")
        print(f"        • Rejected: {rejected_count}")
        
        # User type breakdown
        staff_count = User.objects.filter(is_staff=True).count()
        superuser_count = User.objects.filter(is_superuser=True).count()
        regular_count = user_count - staff_count
        
        print(f"\n   👥 User Type Breakdown:")
        print(f"      Regular Users: {regular_count}")
        print(f"      Staff Members: {staff_count - superuser_count}")
        print(f"      Superusers: {superuser_count}")
        
        # Application types
        new_apps = NRCApplication.objects.filter(application_type='new').count()
        replacement_apps = NRCApplication.objects.filter(application_type='replacement').count()
        
        print(f"\n   📋 Application Types:")
        print(f"      New NRC: {new_apps}")
        print(f"      Replacements: {replacement_apps}")
        
        # Recent activity
        from django.utils import timezone
        from datetime import timedelta
        
        recent_apps = NRCApplication.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        print(f"\n   📈 Recent Activity (Last 7 days):")
        print(f"      New Applications: {recent_apps}")
        
    except Exception as e:
        print(f"   ❌ Error getting statistics: {e}")

def show_indexes():
    """Show database indexes"""
    print(f"\n🔍 DATABASE INDEXES")
    print("-" * 40)
    
    indexes = [
        "accounts_customuser_username (UNIQUE)",
        "accounts_customuser_email",
        "accounts_customuser_nrc_number (UNIQUE)",
        "applications_nrcapplication_user_id (FK)",
        "applications_nrcapplication_status",
        "applications_nrcapplication_created_at",
        "applications_nrcapplication_nrc_number (UNIQUE)"
    ]
    
    for index in indexes:
        print(f"   📇 {index}")

if __name__ == '__main__':
    analyze_database_schema()
    show_indexes()
    
    print(f"\n🎯 SCHEMA SUMMARY")
    print("-" * 40)
    print("   • 2 Main Models: CustomUser, NRCApplication")
    print("   • 1 Primary Relationship: User → Applications (1:N)")
    print("   • 3 User Types: Citizens, Staff, Superusers")
    print("   • Modern Features: OTP verification, Digital signatures, Barcodes")
    print("   • Security: Multi-layered authentication & authorization")
    print("\n✅ Database schema analysis complete!")