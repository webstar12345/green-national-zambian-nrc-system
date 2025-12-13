"""
OTP Service for NRC System
Handles OTP generation, validation, and email sending
"""
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class OTPService:
    """Service class for OTP operations"""
    
    @staticmethod
    def generate_otp_code():
        """Generate a 6-digit OTP code"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def send_otp_email(email, otp_code, user_name=None):
        """Send OTP code via email with HTML template"""
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.conf import settings
        
        subject = 'NRC Zambia - Verification Code'
        
        # Plain text version
        text_message = f"""
Hello {user_name or 'User'},

Your verification code for NRC Zambia is: {otp_code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
NRC Zambia Team
        """
        
        # HTML version
        try:
            html_message = render_to_string('accounts/otp_email.html', {
                'user_name': user_name or 'User',
                'otp_code': otp_code,
            })
        except Exception as e:
            print(f"Failed to render HTML template: {e}")
            html_message = None
        
        try:
            # Create email with both text and HTML versions
            email_msg = EmailMultiAlternatives(
                subject,
                text_message,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            
            if html_message:
                email_msg.attach_alternative(html_message, "text/html")
            
            email_msg.send(fail_silently=False)
            return True
            
        except Exception as e:
            print(f"Failed to send OTP email: {e}")
            return False
    
    @staticmethod
    def is_otp_expired(otp_created_at, expiry_minutes=10):
        """Check if OTP is expired"""
        if not otp_created_at:
            return True
        
        expiry_time = otp_created_at + timedelta(minutes=expiry_minutes)
        return timezone.now() > expiry_time
    
    @staticmethod
    def validate_otp_format(otp_code):
        """Validate OTP format (6 digits)"""
        if not otp_code:
            return False
        
        return len(otp_code) == 6 and otp_code.isdigit()


def send_otp_email(email, otp_code, user_name=None):
    """Backward compatibility function"""
    return OTPService.send_otp_email(email, otp_code, user_name)