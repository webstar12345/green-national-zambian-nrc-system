#!/usr/bin/env python
"""
Fix migration dependency issues for Render deployment
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def fix_migration_issues():
    """Fix migration dependency issues"""
    print("🔧 Fixing migration dependency issues...")
    
    try:
        # First, let's see what migrations Django thinks exist
        print("\n📋 Checking migration status...")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
    except Exception as e:
        print(f"❌ Error checking migrations: {e}")
        
        # Try to reset migration state
        print("\n🔄 Attempting to fix migration state...")
        
        # Clear migration records for problematic apps
        with connection.cursor() as cursor:
            try:
                # Remove problematic migration records
                cursor.execute("""
                    DELETE FROM django_migrations 
                    WHERE app = 'accounts' AND name LIKE '%0004_add_otp_fields_fixed%'
                """)
                
                cursor.execute("""
                    DELETE FROM django_migrations 
                    WHERE app = 'accounts' AND name LIKE '%0014_auto_20241101_1234%'
                """)
                
                print("✅ Cleared problematic migration records")
                
            except Exception as db_error:
                print(f"⚠️  Database cleanup failed: {db_error}")
        
        # Try fake migrations to fix state
        try:
            print("\n🎭 Attempting to fake migrate to fix state...")
            execute_from_command_line(['manage.py', 'migrate', 'accounts', '--fake'])
            execute_from_command_line(['manage.py', 'migrate', 'applications', '--fake'])
            
        except Exception as fake_error:
            print(f"⚠️  Fake migration failed: {fake_error}")

if __name__ == '__main__':
    fix_migration_issues()