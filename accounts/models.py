from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
import string

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    nrc_number = models.CharField(max_length=20, blank=True, unique=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # OTP fields for Google OAuth
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    def get_initials(self):
        """Get user initials for avatar placeholder"""
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.username[0].upper() if self.username else "U"
    
    def generate_otp(self):
        """Generate a 6-digit OTP code"""
        self.otp_code = ''.join(random.choices(string.digits, k=6))
        self.otp_created_at = timezone.now()
        self.otp_verified = False
        self.save()
        return self.otp_code
    
    def verify_otp(self, code):
        """Verify OTP code (valid for 10 minutes)"""
        if not self.otp_code or not self.otp_created_at:
            return False
        
        # Check if OTP is expired (10 minutes)
        time_diff = timezone.now() - self.otp_created_at
        if time_diff.total_seconds() > 600:  # 10 minutes
            return False
        
        # Check if code matches
        if self.otp_code == code:
            self.otp_verified = True
            self.otp_code = None  # Clear OTP after verification
            self.save()
            return True
        
        return False