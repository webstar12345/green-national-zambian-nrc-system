from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class NotificationService:
    """Service class for creating and managing notifications"""
    
    @staticmethod
    def create_approval_notification(application):
        """Create notification when application is approved"""
        from .models import Notification
        notification = Notification.objects.create(
            user=application.user,
            notification_type='application_approved',
            title='🎉 Your NRC Application Has Been Approved!',
            message=f'Congratulations! Your NRC application (#{application.id:05d}) has been approved. '
                   f'Your NRC number is {application.nrc_number}. You can now download your NRC card.',
            application=application
        )
        return notification
    
    @staticmethod
    def create_new_application_notification(application):
        """Create notification for admin users when a new application is submitted"""
        from .models import Notification
        
        # Get all admin users (staff and superusers)
        admin_users = User.objects.filter(
            models.Q(is_staff=True) | models.Q(is_superuser=True)
        )
        
        notifications = []
        for admin_user in admin_users:
            notification = Notification.objects.create(
                user=admin_user,
                notification_type='new_application_submitted',
                title=f'📋 New {application.get_application_type_display()} Application Submitted',
                message=f'A new {application.application_type} NRC application has been submitted by '
                       f'{application.user.get_full_name()} ({application.user.email}). '
                       f'Application ID: #{application.id:05d}. Please review and process.',
                application=application,
                is_admin_notification=True
            )
            notifications.append(notification)
        
        return notifications
    
    @staticmethod
    def create_rejection_notification(application, reason=""):
        """Create notification when application is rejected"""
        from .models import Notification
        message = f'Your NRC application (#{application.id:05d}) has been rejected.'
        if reason:
            message += f' Reason: {reason}'
        message += ' Please review the admin notes and contact support if needed.'
        
        notification = Notification.objects.create(
            user=application.user,
            notification_type='application_rejected',
            title='❌ Your NRC Application Has Been Rejected',
            message=message,
            application=application
        )
        return notification
    
    @staticmethod
    def create_nrc_ready_notification(application):
        """Create notification when NRC card is generated and ready"""
        from .models import Notification
        notification = Notification.objects.create(
            user=application.user,
            notification_type='nrc_ready',
            title='📄 Your NRC Card is Ready for Download!',
            message=f'Your NRC card (Number: {application.nrc_number}) has been generated and is ready for download. '
                   f'You can now view and download your official NRC card.',
            application=application
        )
        return notification
    
    @staticmethod
    def get_unread_notifications(user):
        """Get all unread notifications for a user"""
        from .models import Notification
        return Notification.objects.filter(user=user, is_read=False)
    
    @staticmethod
    def get_admin_notifications(user, limit=10):
        """Get recent admin notifications for admin users"""
        from .models import Notification
        if not (user.is_staff or user.is_superuser):
            return Notification.objects.none()
        
        return Notification.objects.filter(
            user=user, 
            is_admin_notification=True
        ).order_by('-created_at')[:limit]
    
    @staticmethod
    def get_unread_admin_notifications(user):
        """Get unread admin notifications for admin users"""
        from .models import Notification
        if not (user.is_staff or user.is_superuser):
            return Notification.objects.none()
        
        return Notification.objects.filter(
            user=user, 
            is_admin_notification=True,
            is_read=False
        )
    
    @staticmethod
    def mark_as_read(notification_id, user):
        """Mark a notification as read"""
        from .models import Notification
        try:
            notification = Notification.objects.get(id=notification_id, user=user)
            notification.is_read = True
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for a user"""
        from .models import Notification
        Notification.objects.filter(user=user, is_read=False).update(is_read=True)