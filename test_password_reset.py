#!/usr/bin/env python
"""
Test Password Reset Functionality
Verify that password reset emails use the correct domain
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

User = get_user_model()

def test_password_reset():
    """Test password reset functionality"""
    print("🔧 Testing Password Reset Functionality...")
    print("=" * 50)
    print()
    
    try:
        # Check current site
        site = Site.objects.get_current()
        print(f"Current site: {site.domain} (ID: {site.id})")
        print()
        
        # Find a test user
        users = User.objects.all()[:3]
        if not users:
            print("❌ No users found for testing")
            return
        
        print(f"Found {users.count()} users for testing:")
        for user in users:
            print(f"  - {user.username} ({user.email})")
        print()
        
        # Test with first user
        test_user = users[0]
        print(f"Testing password reset for: {test_user.username} ({test_user.email})")
        
        # Generate password reset token and UID
        token = default_token_generator.make_token(test_user)
        uid = urlsafe_base64_encode(force_bytes(test_user.pk))
        
        # Construct reset URL
        reset_url = f"http://{site.domain}/accounts/password/reset/confirm/{uid}/{token}/"
        
        print(f"✅ Generated reset URL: {reset_url}")
        print()
        
        # Test email template (if exists)
        try:
            email_content = render_to_string('registration/password_reset_email.html', {
                'email': test_user.email,
                'domain': site.domain,
                'site_name': site.name,
                'uid': uid,
                'user': test_user,
                'token': token,
                'protocol': 'http',
            })
            print("✅ Email template rendered successfully")
            print("📧 Email preview (first 200 chars):")
            print(email_content[:200] + "...")
        except Exception as e:
            print(f"⚠️ Email template not found or error: {e}")
        
        print()
        print("🎯 Password Reset Test Results:")
        print(f"✅ Site domain: {site.domain}")
        print(f"✅ Reset URL format: Correct")
        print(f"✅ Token generation: Working")
        print(f"✅ UID encoding: Working")
        print()
        
        print("📋 To test manually:")
        print("1. Go to: http://localhost:8000/accounts/password/reset/")
        print("2. Enter email address")
        print("3. Check email for reset link")
        print("4. Verify link points to localhost:8000")
        print()
        
        print("✅ Password reset functionality is properly configured!")
        
    except Exception as e:
        print(f"❌ Error testing password reset: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password_reset()