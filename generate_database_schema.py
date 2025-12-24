#!/usr/bin/env python
"""
Database Schema Generator for Zambian NRC System
Generates detailed database schema information and relationships
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.apps import apps
from django.db import models
from django.contrib.auth import get_user_model

def analyze_model_relationships():
    """Analyze all models and their relationships"""
    
    print("🗃️  ZAMBIAN NRC SYSTEM - DATABASE SCHEMA ANALYSIS")
    print("=" * 80)
    
    # Get all models from our apps
    app_models = {}
    for app_name in ['accounts', 'applications']:
        app_models[app_name] = list(apps.get_app_config(app_name).get_models())
    
    print(f"\n📊 APPLICATIONS OVERVIEW")
    print("-" * 40)
    for app_name, models_list in app_models.items():
        print(f"📱 {app_name.upper()} App: {len(models_list)} models")
        for model in models_list:
            print(f"   └── {model.__name__}")
    
    print(f"\n🔗 DETAILED MODEL ANALYSIS")
    print("-" * 40)
    
    for app_name, models_list in app_models.items():
        print(f"\n📱 {app_name.upper()} APP MODELS:")
        print("=" * 50)
        
        for model in models_list:
            analyze_single_model(model)

def analyze_single_model(model):
    """Analyze a single model's fields and relationships"""
    
    print(f"\n🏗️  MODEL: {model.__name__}")
    print("-" * 30)
    
    # Get all fields
    fields = model._meta.get_fields()
    
    # Categorize fields
    regular_fields = []
    foreign_keys = []
    reverse_relations = []
    
    for field in fields:
        if isinstance(field, models.ForeignKey):
            foreign_keys.append(field)
        elif hasattr(field, 'related_model') and field.related_model:
            reverse_relations.append(field)
        else:
            regular_fields.append(field)
    
    # Display regular fields
    print("📋 FIELDS:")
    for field in regular_fields:
        field_type = type(field).__name__
        field_info = f"   {field.name} ({field_type}"
        
        # Add field constraints
        constraints = []
        if hasattr(field, 'max_length') and field.max_length:
            constraints.append(f"max_length={field.max_length}")
        if hasattr(field, 'unique') and field.unique:
            constraints.append("UNIQUE")
        if hasattr(field, 'null') and not field.null:
            constraints.append("NOT NULL")
        if hasattr(field, 'blank') and not field.blank:
            constraints.append("REQUIRED")
        if hasattr(field, 'default') and field.default != models.NOT_PROVIDED:
            constraints.append(f"default={field.default}")
        
        if constraints:
            field_info += f", {', '.join(constraints)}"
        field_info += ")"
        
        print(field_info)
    
    # Display foreign key relationships
    if foreign_keys:
        print("\n🔗 FOREIGN KEY RELATIONSHIPS:")
        for fk in foreign_keys:
            related_model = fk.related_model.__name__
            on_delete = fk.remote_field.on_delete.__name__ if hasattr(fk.remote_field, 'on_delete') else 'CASCADE'
            print(f"   {fk.name} → {related_model} (ON DELETE {on_delete})")
    
    # Display reverse relationships
    if reverse_relations:
        print("\n🔄 REVERSE RELATIONSHIPS:")
        for rel in reverse_relations:
            if hasattr(rel, 'related_model'):
                related_model = rel.related_model.__name__
                relation_type = type(rel).__name__
                accessor_name = getattr(rel, 'get_accessor_name', lambda: rel.name)()
                print(f"   ← {related_model}.{accessor_name} ({relation_type})")
    
    # Display model metadata
    print(f"\n📊 METADATA:")
    print(f"   Table Name: {model._meta.db_table}")
    print(f"   Verbose Name: {model._meta.verbose_name}")
    if model._meta.ordering:
        print(f"   Default Ordering: {model._meta.ordering}")
    
    # Display model methods
    custom_methods = [method for method in dir(model) 
                     if not method.startswith('_') 
                     and callable(getattr(model, method))
                     and method not in ['objects', 'DoesNotExist', 'MultipleObjectsReturned']]
    
    if custom_methods:
        print(f"\n🔧 CUSTOM METHODS:")
        for method in custom_methods[:10]:  # Show first 10 methods
            print(f"   {method}()")

def generate_relationship_summary():
    """Generate a summary of all relationships in the system"""
    
    print(f"\n\n🔗 RELATIONSHIP SUMMARY")
    print("=" * 50)
    
    User = get_user_model()
    
    relationships = [
        {
            'from': 'CustomUser',
            'to': 'NRCApplication',
            'type': '1:N',
            'description': 'One user can have multiple NRC applications',
            'field': 'user',
            'cascade': 'CASCADE'
        },
        {
            'from': 'CustomUser',
            'to': 'Notification',
            'type': '1:N',
            'description': 'One user can receive multiple notifications',
            'field': 'user',
            'cascade': 'CASCADE'
        },
        {
            'from': 'CustomUser',
            'to': 'DuplicationLog',
            'type': '1:N',
            'description': 'One user can have multiple duplication logs',
            'field': 'user',
            'cascade': 'CASCADE'
        },
        {
            'from': 'CustomUser',
            'to': 'DuplicationLog',
            'type': '1:N',
            'description': 'One admin can handle multiple duplication cases',
            'field': 'admin_user',
            'cascade': 'SET_NULL'
        },
        {
            'from': 'NRCApplication',
            'to': 'Notification',
            'type': '1:N',
            'description': 'One application can generate multiple notifications',
            'field': 'application',
            'cascade': 'CASCADE'
        }
    ]
    
    for rel in relationships:
        print(f"\n📊 {rel['from']} → {rel['to']} ({rel['type']})")
        print(f"   Description: {rel['description']}")
        print(f"   Field: {rel['field']}")
        print(f"   On Delete: {rel['cascade']}")

def generate_sql_schema():
    """Generate SQL CREATE statements for the schema"""
    
    print(f"\n\n💾 SQL SCHEMA GENERATION")
    print("=" * 50)
    
    from django.core.management import call_command
    from io import StringIO
    
    # Generate SQL for all migrations
    print("📝 SQL CREATE STATEMENTS:")
    print("-" * 30)
    
    try:
        # This would show the SQL for creating tables
        sql_output = StringIO()
        call_command('sqlmigrate', 'accounts', '0001', stdout=sql_output)
        print("🔧 Accounts App SQL:")
        print(sql_output.getvalue()[:500] + "..." if len(sql_output.getvalue()) > 500 else sql_output.getvalue())
        
        sql_output = StringIO()
        call_command('sqlmigrate', 'applications', '0001', stdout=sql_output)
        print("\n🔧 Applications App SQL:")
        print(sql_output.getvalue()[:500] + "..." if len(sql_output.getvalue()) > 500 else sql_output.getvalue())
        
    except Exception as e:
        print(f"⚠️  Could not generate SQL: {e}")
        print("💡 Run 'python manage.py sqlmigrate <app> <migration>' manually for SQL output")

def display_current_data_stats():
    """Display current database statistics"""
    
    print(f"\n\n📊 CURRENT DATABASE STATISTICS")
    print("=" * 50)
    
    try:
        User = get_user_model()
        from applications.models import NRCApplication, Notification, DuplicationLog
        
        # User statistics
        total_users = User.objects.count()
        admin_users = User.objects.filter(models.Q(is_staff=True) | models.Q(is_superuser=True)).count()
        regular_users = total_users - admin_users
        
        print(f"👥 USERS:")
        print(f"   Total Users: {total_users}")
        print(f"   Admin Users: {admin_users}")
        print(f"   Regular Users: {regular_users}")
        
        # Application statistics
        total_apps = NRCApplication.objects.count()
        pending_apps = NRCApplication.objects.filter(status='pending').count()
        approved_apps = NRCApplication.objects.filter(status='approved').count()
        rejected_apps = NRCApplication.objects.filter(status='rejected').count()
        new_apps = NRCApplication.objects.filter(application_type='new').count()
        replacement_apps = NRCApplication.objects.filter(application_type='replacement').count()
        
        print(f"\n📋 APPLICATIONS:")
        print(f"   Total Applications: {total_apps}")
        print(f"   Pending: {pending_apps}")
        print(f"   Approved: {approved_apps}")
        print(f"   Rejected: {rejected_apps}")
        print(f"   New NRC: {new_apps}")
        print(f"   Replacements: {replacement_apps}")
        
        # Notification statistics
        total_notifications = Notification.objects.count()
        unread_notifications = Notification.objects.filter(is_read=False).count()
        admin_notifications = Notification.objects.filter(is_admin_notification=True).count()
        
        print(f"\n🔔 NOTIFICATIONS:")
        print(f"   Total Notifications: {total_notifications}")
        print(f"   Unread: {unread_notifications}")
        print(f"   Admin Notifications: {admin_notifications}")
        
        # Duplication log statistics
        total_logs = DuplicationLog.objects.count()
        
        print(f"\n🛡️  SECURITY LOGS:")
        print(f"   Duplication Logs: {total_logs}")
        
        # Recent activity
        from django.utils import timezone
        from datetime import timedelta
        
        recent_apps = NRCApplication.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        recent_notifications = Notification.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        print(f"\n📈 RECENT ACTIVITY (Last 7 days):")
        print(f"   New Applications: {recent_apps}")
        print(f"   New Notifications: {recent_notifications}")
        
    except Exception as e:
        print(f"⚠️  Could not fetch statistics: {e}")

def main():
    """Main function to run all analyses"""
    
    try:
        analyze_model_relationships()
        generate_relationship_summary()
        display_current_data_stats()
        generate_sql_schema()
        
        print(f"\n\n✅ DATABASE SCHEMA ANALYSIS COMPLETE!")
        print("=" * 50)
        print("📋 Summary:")
        print("   • Entity relationships documented")
        print("   • Field specifications analyzed")
        print("   • Current data statistics displayed")
        print("   • SQL schema information provided")
        print("\n💡 For visual ERD, consider using tools like:")
        print("   • Django Extensions (graph_models)")
        print("   • dbdiagram.io")
        print("   • MySQL Workbench")
        print("   • pgAdmin (for PostgreSQL)")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()