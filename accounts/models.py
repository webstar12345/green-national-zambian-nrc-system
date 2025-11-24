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

        # OTP fields for phone/email verification (forced migration)
    otp_code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        default=None,        # ← Changed from "" to None (real change)
        editable=False,      # ← New attribute Django can't ignore
        verbose_name="OTP Code",
        help_text="Temporary 6-digit code"
    )
    otp_created_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,        # ← Changed from timezone.now to None
        editable=False,
        verbose_name="OTP Created At"
    )
    otp_verified = models.BooleanField(
        default=False,
        verbose_name="OTP Verified",
        editable=False       # ← Also added here
    )
    
    def __str__(self):
        return self.username

    def get_initials(self):
        """
        Return initials for use in placeholder avatars.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.username[0].upper() if self.username else "U"

    def generate_otp(self):
        """
        Generate a 6-digit OTP and update fields.
        """
        self.otp_code = ''.join(random.choices(string.digits, k=6))
        self.otp_created_at = timezone.now()
        self.otp_verified = False
        self.save()
        return self.otp_code

    def verify_otp(self, code):
        """
        Validate OTP (must not be expired and must match).
        """
        if not self.otp_code or not self.otp_created_at:
            return False

        # Check expiration (10 minutes)
        if (timezone.now() - self.otp_created_at).total_seconds() > 600:
            return False

        # Check code match
        if self.otp_code == code:
            self.otp_verified = True
            self.otp_code = None  # Clear after success
            self.save()
            return True

        return False
