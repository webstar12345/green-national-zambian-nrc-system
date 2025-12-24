from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import NRCApplication
from .duplication_prevention import DuplicationChecker, DuplicationPreventionMixin

User = get_user_model()

class NRCApplicationForm(forms.ModelForm, DuplicationPreventionMixin):
    class Meta:
        model = NRCApplication
        fields = [
            'village', 'district', 'date_of_birth', 'place_of_birth', 'chief_name', 'sex', 'photo',
            'mother_full_name', 'mother_village', 'mother_district', 'mother_date_of_birth', 'mother_place_of_birth', 'mother_chief_name',
            'father_full_name', 'father_village', 'father_district', 'father_date_of_birth', 'father_place_of_birth', 'father_chief_name',
            'birth_certificate', 'under_five_card'
        ]
        
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'mother_date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'father_date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'application_type': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'village': 'Your Village',
            'district': 'Your District',
            'date_of_birth': 'Your Date of Birth',
            'place_of_birth': 'Your Place of Birth',
            'chief_name': 'Your Chief Name',
            'sex': 'Sex/Gender',
            'photo': 'Your Photo (Passport Size)',
            'mother_full_name': "Mother's Full Name",
            'mother_village': "Mother's Village",
            'mother_district': "Mother's District",
            'mother_date_of_birth': "Mother's Date of Birth",
            'mother_place_of_birth': "Mother's Place of Birth",
            'mother_chief_name': "Mother's Chief Name",
            'father_full_name': "Father's Full Name",
            'father_village': "Father's Village",
            'father_district': "Father's District",
            'father_date_of_birth': "Father's Date of Birth",
            'father_place_of_birth': "Father's Place of Birth",
            'father_chief_name': "Father's Chief Name",
            'birth_certificate': 'Birth Certificate (PDF)',
            'under_five_card': 'Under Five Card (PDF)',
            'old_nrc': 'Old NRC (PDF) - Required for replacement only',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
        # Make photo field not required
        self.fields['photo'].required = False
    
    def clean(self):
        """
        Perform comprehensive duplication checking
        """
        cleaned_data = super().clean()
        
        if not self.user:
            raise ValidationError("User information is required for duplication checking.")
        
        # Prepare application data for duplication check
        application_data = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'date_of_birth': cleaned_data.get('date_of_birth'),
            'place_of_birth': cleaned_data.get('place_of_birth'),
            'mother_full_name': cleaned_data.get('mother_full_name'),
            'mother_date_of_birth': cleaned_data.get('mother_date_of_birth'),
            'father_full_name': cleaned_data.get('father_full_name'),
            'father_date_of_birth': cleaned_data.get('father_date_of_birth'),
            'sex': cleaned_data.get('sex'),
            'village': cleaned_data.get('village'),
        }
        
        # Check for duplicates (exclude current instance if editing)
        exclude_id = self.instance.id if self.instance and self.instance.pk else None
        
        try:
            self.validate_no_duplicates(application_data, self.user, exclude_id)
        except ValidationError as e:
            # Add duplication errors to form errors
            raise ValidationError({
                '__all__': e.messages
            })
        
        return cleaned_data

class NRCReplacementForm(forms.ModelForm, DuplicationPreventionMixin):
    class Meta:
        model = NRCApplication
        fields = [
            'old_nrc', 'birth_certificate', 'under_five_card', 'replacement_reason'
        ]
        
        labels = {
            'old_nrc': 'Old/Damaged NRC (PDF)',
            'birth_certificate': 'Birth Certificate (PDF)',
            'under_five_card': 'Under Five Card (PDF)',
            'replacement_reason': 'Reason for Replacement',
        }
        
        widgets = {
            'replacement_reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Please provide a detailed reason for NRC replacement (e.g., lost, damaged, stolen, etc.)'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
        # All fields are required for replacement
        self.fields['old_nrc'].required = True
        self.fields['replacement_reason'].required = True
    
    def clean(self):
        """
        Validate replacement application and check for existing approved NRC
        """
        cleaned_data = super().clean()
        
        if not self.user:
            raise ValidationError("User information is required for replacement validation.")
        
        # Check if user has an existing approved NRC (required for replacement)
        has_nrc, existing_app = DuplicationChecker.check_user_existing_nrc(self.user)
        
        if not has_nrc:
            raise ValidationError({
                '__all__': [
                    "You must have an existing approved NRC to apply for a replacement. "
                    "Please apply for a new NRC instead."
                ]
            })
        
        # Check if user already has a pending replacement application
        pending_replacements = NRCApplication.objects.filter(
            user=self.user,
            application_type='replacement',
            status='pending'
        )
        
        # Exclude current instance if editing
        if self.instance and self.instance.pk:
            pending_replacements = pending_replacements.exclude(id=self.instance.id)
        
        if pending_replacements.exists():
            raise ValidationError({
                '__all__': [
                    f"You already have a pending replacement application (#{pending_replacements.first().id:05d}). "
                    "Please wait for it to be processed before submitting another replacement."
                ]
            })
        
        return cleaned_data

class AdminApplicationForm(forms.ModelForm):
    class Meta:
        model = NRCApplication
        fields = ['status', 'admin_notes']
        
        widgets = {
            'admin_notes': forms.Textarea(attrs={'rows': 4}),
        }