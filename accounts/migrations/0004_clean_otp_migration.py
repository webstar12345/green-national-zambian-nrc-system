# Clean OTP Migration - Final Fix
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_otp_code_customuser_otp_created_at_and_more'),
    ]

    operations = [
        # Empty migration - OTP fields already exist from migration 0003
        # This migration exists only to maintain proper migration chain
    ]