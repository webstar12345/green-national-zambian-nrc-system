@echo off
echo ========================================
echo   DEPLOYING ADMIN NOTIFICATION SYSTEM
echo ========================================
echo.

echo 📋 Admin Notification System Features:
echo   ✅ Admin users receive notifications when new applications are submitted
echo   ✅ Separate notification type for new applications
echo   ✅ Admin dashboard shows recent notifications with unread count
echo   ✅ Notifications link directly to application review page
echo   ✅ Both new NRC and replacement applications trigger notifications
echo.

echo 🔄 Running database migrations...
python manage.py makemigrations applications --name add_admin_notifications
python manage.py migrate

echo.
echo 🧪 Testing admin notification system...
python test_admin_notifications.py

echo.
echo 📊 Checking current admin users...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
admins = User.objects.filter(is_staff=True)
print(f'Found {admins.count()} admin users:')
for admin in admins:
    print(f'  - {admin.username} ({admin.email}) - Staff: {admin.is_staff}, Super: {admin.is_superuser}')
"

echo.
echo ✅ ADMIN NOTIFICATION SYSTEM DEPLOYED SUCCESSFULLY!
echo.
echo 📋 How it works:
echo   1. When a user submits a new NRC or replacement application
echo   2. All admin users (is_staff=True or is_superuser=True) receive a notification
echo   3. Notifications appear on the admin dashboard with unread count
echo   4. Clicking the notification takes admin to the application review page
echo   5. Admins can view all notifications in the notifications page
echo.
echo 🎯 Next steps:
echo   1. Submit a test application as a regular user
echo   2. Login as admin to see the notification on dashboard
echo   3. Click notification to review the application
echo.
pause