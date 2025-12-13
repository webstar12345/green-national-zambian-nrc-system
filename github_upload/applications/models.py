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
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.application_type} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']