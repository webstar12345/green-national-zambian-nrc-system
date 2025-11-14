#!/usr/bin/env python3
"""
Setup script for Zambian NRC System
This script will help you set up the project for development
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🇿🇲 Zambian National Registration Card System Setup")
    print("=" * 50)
    
    # Check if Python is available
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please install manually:")
        print("pip install -r requirements.txt")
        return
    
    # Create migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return
    
    # Apply migrations
    if not run_command("python manage.py migrate", "Applying migrations"):
        return
    
    # Create superuser
    print("\n📝 Creating admin superuser...")
    print("Please provide admin credentials:")
    if not run_command("python manage.py createsuperuser", "Creating superuser"):
        print("⚠️  You can create a superuser later with: python manage.py createsuperuser")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Static files collection failed, but the system should still work")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the development server: python manage.py runserver")
    print("2. Open your browser to: http://127.0.0.1:8000")
    print("3. Admin panel: http://127.0.0.1:8000/admin")
    print("\nFeatures available:")
    print("• User registration and authentication")
    print("• NRC application submission (new and replacement)")
    print("• Document upload (PDF)")
    print("• Admin dashboard for application management")
    print("• Application status tracking")
    print("\nEnjoy using the Zambian NRC System! 🇿🇲")

if __name__ == "__main__":
    main()