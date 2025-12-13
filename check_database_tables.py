#!/usr/bin/env python
"""
Script to check database tables and structure
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.db import connection

def check_tables():
    """Check what tables exist in the database"""
    print("🔍 Checking database tables...")
    
    with connection.cursor() as cursor:
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📊 Found {len(tables)} tables:")
        for table in tables:
            table_name = table[0]
            print(f"  - {table_name}")
            
            # Check if it's one of our application tables
            if 'nrc' in table_name.lower() or 'application' in table_name.lower():
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"    Records: {count}")
        
        # Check specifically for our new tables
        new_tables = [
            'applications_newnrcapplication',
            'applications_nrcreplacement',
            'applications_nrcapplication'
        ]
        
        print("\n🎯 Checking for NRC application tables:")
        for table_name in new_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"  ✅ {table_name}: {count} records")
            except Exception as e:
                print(f"  ❌ {table_name}: Not found or error - {e}")

if __name__ == '__main__':
    check_tables()