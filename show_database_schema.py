#!/usr/bin/env python
"""
Script to show database schema for NRC tables
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.db import connection

def show_table_schema(table_name):
    """Show the schema for a specific table"""
    with connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print(f"\n📋 Table: {table_name}")
        print("=" * 60)
        print(f"{'Column':<25} {'Type':<15} {'Null':<6} {'Default':<15}")
        print("-" * 60)
        
        for col in columns:
            cid, name, col_type, notnull, default_val, pk = col
            null_str = "NO" if notnull else "YES"
            default_str = str(default_val) if default_val is not None else ""
            print(f"{name:<25} {col_type:<15} {null_str:<6} {default_str:<15}")

def main():
    """Show schema for all NRC application tables"""
    print("🗄️  NRC System Database Schema")
    print("=" * 60)
    
    # Tables to show
    tables = [
        'applications_newnrcapplication',
        'applications_nrcreplacement', 
        'applications_nrcapplication'
    ]
    
    for table in tables:
        try:
            show_table_schema(table)
        except Exception as e:
            print(f"\n❌ Error showing schema for {table}: {e}")
    
    print(f"\n✅ Schema display complete!")
    print("\n📊 Summary:")
    print("- applications_newnrcapplication: For new NRC applications")
    print("- applications_nrcreplacement: For NRC replacements (has old_nrc and replacement_reason)")
    print("- applications_nrcapplication: Legacy table (kept for compatibility)")

if __name__ == '__main__':
    main()