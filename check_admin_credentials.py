#!/usr/bin/env python
"""
Script to check admin user credentials in the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from accounts.models import CustomUser

def check_admin_credentials():
    print("=" * 60)
    print("CHECKING ADMIN CREDENTIALS")
    print("=" * 60)
    
    # Get all superusers
    superusers = CustomUser.objects.filter(is_superuser=True)
    
    if not superusers.exists():
        print("\n❌ NO ADMIN USERS FOUND!")
        print("\nCreate one with: python manage.py createsuperuser")
        return
    
    print(f"\n✅ Found {superusers.count()} admin user(s):\n")
    
    for user in superusers:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Password: [ENCRYPTED - Cannot be displayed]")
        print(f"Password Hash: {user.password[:50]}...")
        print(f"Full Name: {user.get_full_name() or 'Not set'}")
        print(f"Is Active: {'✅ Yes' if user.is_active else '❌ No'}")
        print(f"Is Staff: {'✅ Yes' if user.is_staff else '❌ No'}")
        print(f"Is Superuser: {'✅ Yes' if user.is_superuser else '❌ No'}")
        print(f"Date Joined: {user.date_joined}")
        print(f"Last Login: {user.last_login or 'Never'}")
        print("-" * 60)
    
    print("\n⚠️  IMPORTANT: Passwords are encrypted and cannot be retrieved!")
    print("Django stores passwords as hashes for security.")
    print("\n💡 To reset a password, use:")
    print("   python manage.py changepassword <username>")
    print("\n💡 Or create a new admin:")
    print("   python manage.py createsuperuser")
    
    # Offer to reset password
    print("\n" + "=" * 60)
    reset = input("\nDo you want to reset a password now? (y/n): ").lower()
    if reset == 'y':
        username = input("Enter username to reset: ").strip()
        try:
            user = CustomUser.objects.get(username=username)
            new_password = input("Enter new password: ")
            user.set_password(new_password)
            user.save()
            print(f"\n✅ Password updated successfully for '{username}'!")
            print(f"\nYou can now login with:")
            print(f"   Username: {username}")
            print(f"   Password: {new_password}")
        except CustomUser.DoesNotExist:
            print(f"\n❌ User '{username}' not found!")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    check_admin_credentials()
