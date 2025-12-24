from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class NRCApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Application Info
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=20, choices=[('new', 'New NRC'), ('replacement', 'Replacement')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Applicant Details
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100, default='Not provided')
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    chief_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], default='M')
    photo = models.ImageField(upload_to='photos/applicants/', help_text='Upload your passport-size photo', blank=True, null=True)
    
    # Mother's Details
    mother_full_name = models.CharField(max_length=200, default='Not provided')
    mother_village = models.CharField(max_length=100)
    mother_district = models.CharField(max_length=100, default='Not provided')
    mother_date_of_birth = models.DateField()
    mother_place_of_birth = models.CharField(max_length=100)
    mother_chief_name = models.CharField(max_length=100)
    
    # Father's Details
    father_full_name = models.CharField(max_length=200, default='Not provided')
    father_village = models.CharField(max_length=100)
    father_district = models.CharField(max_length=100, default='Not provided')
    father_date_of_birth = models.DateField()
    father_place_of_birth = models.CharField(max_length=100)
    father_chief_name = models.CharField(max_length=100)
    
    # Documents
    birth_certificate = models.FileField(upload_to='documents/birth_certificates/')
    under_five_card = models.FileField(upload_to='documents/under_five_cards/')
    old_nrc = models.FileField(upload_to='documents/old_nrc/', blank=True, null=True)  # For replacements
    
    # Replacement specific fields
    replacement_reason = models.TextField(blank=True, help_text='Reason for NRC replacement')
    
    # Admin Notes
    admin_notes = models.TextField(blank=True)
    
    # Generated NRC
    nrc_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    nrc_front_image = models.CharField(max_length=255, blank=True, null=True)
    nrc_back_image = models.CharField(max_length=255, blank=True, null=True)
    nrc_generated_at = models.DateTimeField(blank=True, null=True)
    
    # Digital Signature
    digital_signature = models.TextField(blank=True, null=True, help_text='Base64 encoded signature image')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.application_type} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('application_approved', 'Application Approved'),
        ('application_rejected', 'Application Rejected'),
        ('nrc_ready', 'NRC Card Ready for Download'),
        ('new_application_submitted', 'New Application Submitted'),
        ('system_update', 'System Update'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Flag to identify admin notifications
    is_admin_notification = models.BooleanField(default=False)
    
    # Optional: Link to related application
    application = models.ForeignKey('NRCApplication', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class DuplicationLog(models.Model):
    """
    Log duplicate detection attempts for audit purposes
    """
    DETECTION_TYPES = [
        ('exact_match', 'Exact Match'),
        ('similar_match', 'Similar Match'),
        ('user_existing_nrc', 'User Already Has NRC'),
        ('nrc_number_duplicate', 'NRC Number Duplicate'),
    ]
    
    ACTION_TYPES = [
        ('blocked', 'Application Blocked'),
        ('warned', 'Warning Issued'),
        ('approved_override', 'Admin Override Approved'),
    ]
    
    detected_at = models.DateTimeField(default=timezone.now)
    detection_type = models.CharField(max_length=50, choices=DETECTION_TYPES)
    action_taken = models.CharField(max_length=50, choices=ACTION_TYPES)
    
    # Application details
    attempted_application_data = models.JSONField()
    matching_application_ids = models.JSONField(default=list)
    similarity_scores = models.JSONField(default=list)
    
    # User and admin info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='duplication_logs')
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_duplication_logs')
    admin_notes = models.TextField(blank=True)
    
    # System info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"Duplicate detected: {self.detection_type} - {self.user.username} - {self.detected_at}"