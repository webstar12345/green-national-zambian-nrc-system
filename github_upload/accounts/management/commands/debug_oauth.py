from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Debug OAuth configuration'

    def handle(self, *args, **options):
        self.stdout.write('=== DEBUGGING OAUTH CONFIGURATION ===')
        
        # Check sites
        sites = Site.objects.all()
        self.stdout.write(f'\nSites ({sites.count()}):')
        for site in sites:
            self.stdout.write(f'  ID: {site.id}, Domain: {site.domain}, Name: {site.name}')
        
        # Check all social apps
        apps = SocialApp.objects.all()
        self.stdout.write(f'\nAll Social Apps ({apps.count()}):')
        for app in apps:
            self.stdout.write(f'  ID: {app.id}, Provider: {app.provider}, Name: {app.name}')
            self.stdout.write(f'    Client ID: {app.client_id}')
            self.stdout.write(f'    Sites: {[s.domain for s in app.sites.all()]}')
        
        # Check Google apps specifically
        google_apps = SocialApp.objects.filter(provider='google')
        self.stdout.write(f'\nGoogle Apps ({google_apps.count()}):')
        for app in google_apps:
            self.stdout.write(f'  ID: {app.id}, Name: {app.name}')
            self.stdout.write(f'    Sites: {[s.domain for s in app.sites.all()]}')
        
        # Try to reproduce the error
        try:
            site = Site.objects.get_current()
            self.stdout.write(f'\nCurrent site: {site.domain}')
            
            # This is what allauth does internally
            apps = SocialApp.objects.filter(provider='google', sites=site)
            self.stdout.write(f'Google apps for current site: {apps.count()}')
            
            if apps.count() > 1:
                self.stdout.write(self.style.ERROR('FOUND THE PROBLEM: Multiple Google apps for same site!'))
                for app in apps:
                    self.stdout.write(f'  Duplicate: ID {app.id}, Client ID: {app.client_id}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))