@echo off
echo Setting up new Google OAuth credentials...
python manage.py shell -c "from django.contrib.sites.models import Site; site = Site.objects.get_current(); site.domain = 'localhost:8000'; site.name = 'NRC System'; site.save(); print(f'Site updated: {site.domain}')"
python manage.py shell -c "from allauth.socialaccount.models import SocialApp; from django.contrib.sites.models import Site; import os; SocialApp.objects.filter(provider='google').delete(); app = SocialApp.objects.create(provider='google', name='Google', client_id=os.getenv('GOOGLE_CLIENT_ID', ''), secret=os.getenv('GOOGLE_CLIENT_SECRET', '')); app.sites.add(Site.objects.get_current()); print('Google OAuth app created successfully!')"
echo.
echo Done! Now you can test Google login.
pause
