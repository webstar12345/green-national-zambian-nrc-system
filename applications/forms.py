from django import forms
from .models import NRCApplication

class NRCApplicationForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
        # Make photo field not required
        self.fields['photo'].required = False

class NRCReplacementForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
        # All fields are required for replacement
        self.fields['old_nrc'].required = True
        self.fields['replacement_reason'].required = True

class AdminApplicationForm(forms.ModelForm):
    class Meta:
        model = NRCApplication
        fields = ['status', 'admin_notes']
        
        widgets = {
            'admin_notes': forms.Textarea(attrs={'rows': 4}),
        }