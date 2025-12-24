from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('services/', views.services, name='services'),
    path('apply/', views.apply_nrc, name='apply'),
    path('apply-replacement/', views.apply_replacement, name='apply_replacement'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('application/<int:pk>/', views.application_detail, name='application_detail'),
    path('application/<int:pk>/nrc-card/', views.view_nrc_card, name='view_nrc_card'),
    path('application/<int:pk>/signature/', views.signature_pad, name='signature_pad'),
    
    # NRC Download URLs
    path('application/<int:pk>/download/front/', views.download_nrc_front, name='download_nrc_front'),
    path('application/<int:pk>/download/back/', views.download_nrc_back, name='download_nrc_back'),
    path('application/<int:pk>/download/both/', views.download_nrc_both, name='download_nrc_both'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/applications/', views.admin_applications, name='admin_applications'),
    path('dashboard/application/<int:pk>/', views.admin_application_detail, name='admin_application_detail'),
    path('dashboard/users/', views.admin_users, name='admin_users'),
    path('dashboard/user/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    
    # Report URLs
    path('dashboard/reports/', views.admin_reports, name='admin_reports'),
    path('dashboard/reports/summary/', views.summary_report, name='summary_report'),
    path('dashboard/reports/detailed/', views.detailed_report, name='detailed_report'),
    path('dashboard/reports/exceptions/', views.exception_report, name='exception_report'),
    
    # Officer Dashboard URLs
    path('officer-dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('officer-reports/summary/', views.officer_summary_report, name='officer_summary_report'),
    path('officer-reports/applications/', views.officer_applications_report, name='officer_applications_report'),
    
    # Admin Download URLs
    path('dashboard/application/<int:pk>/download/front/', views.admin_download_nrc_front, name='admin_download_nrc_front'),
    path('dashboard/application/<int:pk>/download/back/', views.admin_download_nrc_back, name='admin_download_nrc_back'),
    path('dashboard/application/<int:pk>/download/both/', views.admin_download_nrc_both, name='admin_download_nrc_both'),
    
    # Notification URLs
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('api/notification-count/', views.get_notification_count, name='notification_count'),
    
    # AI Assistant URLs
    path('api/chat/', views.chat_message, name='chat_message'),
    path('api/quick-responses/', views.get_quick_responses, name='quick_responses'),
    path('ai-demo/', views.ai_demo, name='ai_demo'),
    
    # Duplication Management URLs
    path('dashboard/duplication-check/', views.duplication_check, name='duplication_check'),
    path('admin/mark-not-duplicate/<int:application_id>/', views.mark_not_duplicate, name='mark_not_duplicate'),
]