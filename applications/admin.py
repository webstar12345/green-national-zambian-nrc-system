from django.contrib import admin
from .models import NRCApplication

@admin.register(NRCApplication)
class NRCApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'application_type', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'application_type', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'village', 'chief_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Application Info', {
            'fields': ('user', 'application_type', 'status', 'created_at', 'updated_at')
        }),
        ('Applicant Details', {
            'fields': ('village', 'district', 'date_of_birth', 'place_of_birth', 'chief_name', 'sex', 'photo')
        }),
        ("Mother's Details", {
            'fields': ('mother_full_name', 'mother_village', 'mother_district', 'mother_date_of_birth', 'mother_place_of_birth', 'mother_chief_name')
        }),
        ("Father's Details", {
            'fields': ('father_full_name', 'father_village', 'father_district', 'father_date_of_birth', 'father_place_of_birth', 'father_chief_name')
        }),
        ('Documents', {
            'fields': ('birth_certificate', 'under_five_card', 'old_nrc')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',)
        }),
    )