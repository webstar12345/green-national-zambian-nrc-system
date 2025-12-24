"""
NRC Duplication Prevention System
Comprehensive system to prevent duplicate NRC cards and ensure data integrity
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import NRCApplication
import hashlib
from datetime import datetime, date
from difflib import SequenceMatcher

User = get_user_model()

class DuplicationChecker:
    """
    Comprehensive duplication checker for NRC applications
    Implements multiple layers of duplicate detection
    """
    
    @staticmethod
    def generate_person_hash(application_data):
        """
        Generate a unique hash based on personal identifying information
        This creates a fingerprint for each person to detect duplicates
        """
        # Core identifying information
        identifying_data = {
            'date_of_birth': str(application_data.get('date_of_birth', '')),
            'place_of_birth': application_data.get('place_of_birth', '').lower().strip(),
            'mother_full_name': application_data.get('mother_full_name', '').lower().strip(),
            'mother_date_of_birth': str(application_data.get('mother_date_of_birth', '')),
            'father_full_name': application_data.get('father_full_name', '').lower().strip(),
            'father_date_of_birth': str(application_data.get('father_date_of_birth', '')),
            'sex': application_data.get('sex', '').upper(),
        }
        
        # Create hash string
        hash_string = '|'.join([
            identifying_data['date_of_birth'],
            identifying_data['place_of_birth'],
            identifying_data['mother_full_name'],
            identifying_data['mother_date_of_birth'],
            identifying_data['father_full_name'],
            identifying_data['father_date_of_birth'],
            identifying_data['sex']
        ])
        
        # Generate SHA-256 hash
        return hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    
    @staticmethod
    def check_exact_duplicate(application_data, exclude_application_id=None):
        """
        Check for exact duplicates based on core personal information
        Returns: (is_duplicate, matching_applications)
        """
        filters = {
            'date_of_birth': application_data.get('date_of_birth'),
            'place_of_birth__iexact': application_data.get('place_of_birth', ''),
            'mother_full_name__iexact': application_data.get('mother_full_name', ''),
            'mother_date_of_birth': application_data.get('mother_date_of_birth'),
            'sex': application_data.get('sex', ''),
        }
        
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        matching_apps = NRCApplication.objects.filter(**filters)
        
        # Exclude current application if editing
        if exclude_application_id:
            matching_apps = matching_apps.exclude(id=exclude_application_id)
        
        # Only consider approved applications or pending ones
        matching_apps = matching_apps.filter(
            models.Q(status='approved') | models.Q(status='pending')
        )
        
        return matching_apps.exists(), matching_apps
    
    @staticmethod
    def check_similar_duplicate(application_data, exclude_application_id=None, similarity_threshold=0.85):
        """
        Check for similar duplicates using fuzzy matching
        Returns: (is_similar, similar_applications, similarity_scores)
        """
        # Get all applications with same date of birth and sex (high confidence filters)
        base_filters = {
            'date_of_birth': application_data.get('date_of_birth'),
            'sex': application_data.get('sex', ''),
        }
        
        # Remove None values
        base_filters = {k: v for k, v in base_filters.items() if v is not None}
        
        candidate_apps = NRCApplication.objects.filter(**base_filters)
        
        # Exclude current application if editing
        if exclude_application_id:
            candidate_apps = candidate_apps.exclude(id=exclude_application_id)
        
        # Only consider approved applications or pending ones
        candidate_apps = candidate_apps.filter(
            models.Q(status='approved') | models.Q(status='pending')
        )
        
        similar_apps = []
        similarity_scores = []
        
        for app in candidate_apps:
            # Calculate similarity score
            score = DuplicationChecker.calculate_similarity_score(application_data, app)
            
            if score >= similarity_threshold:
                similar_apps.append(app)
                similarity_scores.append(score)
        
        return len(similar_apps) > 0, similar_apps, similarity_scores
    
    @staticmethod
    def calculate_similarity_score(data1, application2):
        """
        Calculate similarity score between two applications
        Returns: float between 0 and 1 (1 = identical)
        """
        scores = []
        
        # Compare names (high weight)
        if hasattr(application2, 'user'):
            name1 = f"{data1.get('first_name', '')} {data1.get('last_name', '')}".lower().strip()
            name2 = f"{application2.user.first_name} {application2.user.last_name}".lower().strip()
            name_score = SequenceMatcher(None, name1, name2).ratio()
            scores.append(('name', name_score, 0.3))  # 30% weight
        
        # Compare mother's name (high weight)
        mother1 = data1.get('mother_full_name', '').lower().strip()
        mother2 = application2.mother_full_name.lower().strip()
        mother_score = SequenceMatcher(None, mother1, mother2).ratio()
        scores.append(('mother', mother_score, 0.25))  # 25% weight
        
        # Compare father's name (high weight)
        father1 = data1.get('father_full_name', '').lower().strip()
        father2 = application2.father_full_name.lower().strip()
        father_score = SequenceMatcher(None, father1, father2).ratio()
        scores.append(('father', father_score, 0.25))  # 25% weight
        
        # Compare place of birth (medium weight)
        place1 = data1.get('place_of_birth', '').lower().strip()
        place2 = application2.place_of_birth.lower().strip()
        place_score = SequenceMatcher(None, place1, place2).ratio()
        scores.append(('place', place_score, 0.1))  # 10% weight
        
        # Compare village (medium weight)
        village1 = data1.get('village', '').lower().strip()
        village2 = application2.village.lower().strip()
        village_score = SequenceMatcher(None, village1, village2).ratio()
        scores.append(('village', village_score, 0.1))  # 10% weight
        
        # Calculate weighted average
        total_score = sum(score * weight for _, score, weight in scores)
        
        return total_score
    
    @staticmethod
    def check_user_existing_nrc(user, exclude_application_id=None):
        """
        Check if user already has an approved NRC application
        Returns: (has_nrc, existing_application)
        """
        existing_apps = NRCApplication.objects.filter(
            user=user,
            status='approved'
        )
        
        # Exclude current application if editing
        if exclude_application_id:
            existing_apps = existing_apps.exclude(id=exclude_application_id)
        
        if existing_apps.exists():
            return True, existing_apps.first()
        
        return False, None
    
    @staticmethod
    def check_nrc_number_duplicate(nrc_number, exclude_application_id=None):
        """
        Check if NRC number already exists
        Returns: (is_duplicate, existing_application)
        """
        if not nrc_number:
            return False, None
        
        existing_apps = NRCApplication.objects.filter(nrc_number=nrc_number)
        
        # Exclude current application if editing
        if exclude_application_id:
            existing_apps = existing_apps.exclude(id=exclude_application_id)
        
        if existing_apps.exists():
            return True, existing_apps.first()
        
        return False, None
    
    @staticmethod
    def comprehensive_duplicate_check(application_data, user=None, exclude_application_id=None):
        """
        Perform comprehensive duplicate check
        Returns: {
            'is_duplicate': bool,
            'duplicate_type': str,
            'matching_applications': list,
            'similarity_scores': list,
            'recommendations': list
        }
        """
        result = {
            'is_duplicate': False,
            'duplicate_type': None,
            'matching_applications': [],
            'similarity_scores': [],
            'recommendations': []
        }
        
        # 1. Check if user already has approved NRC
        if user:
            has_nrc, existing_app = DuplicationChecker.check_user_existing_nrc(
                user, exclude_application_id
            )
            if has_nrc:
                result['is_duplicate'] = True
                result['duplicate_type'] = 'user_existing_nrc'
                result['matching_applications'] = [existing_app]
                result['recommendations'].append(
                    f"User already has an approved NRC (#{existing_app.nrc_number}). "
                    "Consider applying for replacement instead."
                )
                return result
        
        # 2. Check for exact duplicates
        is_exact, exact_matches = DuplicationChecker.check_exact_duplicate(
            application_data, exclude_application_id
        )
        if is_exact:
            result['is_duplicate'] = True
            result['duplicate_type'] = 'exact_match'
            result['matching_applications'] = list(exact_matches)
            result['recommendations'].append(
                "Exact match found with existing application(s). "
                "This person may already have an NRC or pending application."
            )
            return result
        
        # 3. Check for similar duplicates
        is_similar, similar_matches, scores = DuplicationChecker.check_similar_duplicate(
            application_data, exclude_application_id
        )
        if is_similar:
            result['is_duplicate'] = True
            result['duplicate_type'] = 'similar_match'
            result['matching_applications'] = similar_matches
            result['similarity_scores'] = scores
            result['recommendations'].append(
                "Similar application(s) found. Please verify this is not a duplicate person."
            )
            return result
        
        # 4. Check NRC number if provided
        nrc_number = application_data.get('nrc_number')
        if nrc_number:
            is_nrc_dup, nrc_match = DuplicationChecker.check_nrc_number_duplicate(
                nrc_number, exclude_application_id
            )
            if is_nrc_dup:
                result['is_duplicate'] = True
                result['duplicate_type'] = 'nrc_number_duplicate'
                result['matching_applications'] = [nrc_match]
                result['recommendations'].append(
                    f"NRC number {nrc_number} already exists. "
                    "Please generate a new unique NRC number."
                )
                return result
        
        return result


class DuplicationPreventionMixin:
    """
    Mixin to add duplication prevention to NRC application forms and views
    """
    
    def validate_no_duplicates(self, application_data, user=None, exclude_application_id=None):
        """
        Validate that the application doesn't create duplicates
        Raises ValidationError if duplicates found
        """
        check_result = DuplicationChecker.comprehensive_duplicate_check(
            application_data, user, exclude_application_id
        )
        
        if check_result['is_duplicate']:
            error_messages = []
            
            if check_result['duplicate_type'] == 'user_existing_nrc':
                error_messages.append(
                    "You already have an approved NRC application. "
                    "If you need a replacement, please use the replacement form."
                )
            
            elif check_result['duplicate_type'] == 'exact_match':
                matching_apps = check_result['matching_applications']
                app_ids = [f"#{app.id:05d}" for app in matching_apps]
                error_messages.append(
                    f"An identical application already exists (Application IDs: {', '.join(app_ids)}). "
                    "This person may already have an NRC or pending application."
                )
            
            elif check_result['duplicate_type'] == 'similar_match':
                matching_apps = check_result['matching_applications']
                scores = check_result['similarity_scores']
                app_details = []
                for app, score in zip(matching_apps, scores):
                    app_details.append(f"#{app.id:05d} ({score:.1%} similar)")
                
                error_messages.append(
                    f"Similar applications found: {', '.join(app_details)}. "
                    "Please verify this is not a duplicate person."
                )
            
            elif check_result['duplicate_type'] == 'nrc_number_duplicate':
                matching_app = check_result['matching_applications'][0]
                error_messages.append(
                    f"NRC number already exists in application #{matching_app.id:05d}. "
                    "Please generate a new unique NRC number."
                )
            
            # Add recommendations
            error_messages.extend(check_result['recommendations'])
            
            raise ValidationError(error_messages)
        
        return True


def log_duplication_attempt(detection_result, user, request=None, admin_user=None, action='blocked', admin_notes=''):
    """
    Log a duplication detection attempt
    """
    from .models import DuplicationLog
    
    log_entry = DuplicationLog.objects.create(
        detection_type=detection_result['duplicate_type'],
        action_taken=action,
        attempted_application_data=detection_result.get('application_data', {}),
        matching_application_ids=[app.id for app in detection_result['matching_applications']],
        similarity_scores=detection_result['similarity_scores'],
        user=user,
        admin_user=admin_user,
        admin_notes=admin_notes,
        ip_address=request.META.get('REMOTE_ADDR') if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT', '') if request else '',
    )
    
    return log_entry