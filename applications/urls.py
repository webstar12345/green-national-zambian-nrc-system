from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('services/', views.services, name='services'),
    path('apply/', views.apply_nrc, name='apply'),
    path('apply-replacement/', views.apply_replacement, name='apply_replacement'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('application/<int:pk>/', views.application_detail, name='application_detail'),
    path('application/<int:pk>/nrc-card/', views.view_nrc_card, name='view_nrc_card'),
    
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
    
    # AI Assistant URLs
    path('api/chat/', views.chat_message, name='chat_message'),
    path('api/quick-responses/', views.get_quick_responses, name='quick_responses'),
    path('ai-demo/', views.ai_demo, name='ai_demo'),
]