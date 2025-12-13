from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from decouple import config

class Command(BaseCommand):
    help = 'Setup Google OAuth configuration automatically'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Google OAuth...')
        
        # Get or create site
        try:
            site = Site.objects.get(pk=1)
        except Site.DoesNotExist:
            site = Site.objects.create(pk=1)
        
        # Update site details
        site.domain = config('SITE_DOMAIN', default='nrccard.onrender.com')
        site.name = 'Zambian NRC System'
        site.save()
        self.stdout.write(self.style.SUCCESS(f'✓ Site configured: {site.domain}'))
        
        # Get credentials from environment
        client_id = config('GOOGLE_CLIENT_ID', default='')
        client_secret = config('GOOGLE_CLIENT_SECRET', default='')
        
        if not client_id or not client_secret:
            self.stdout.write(self.style.WARNING(
                '⚠ Warning: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not found in environment variables'
            ))
            self.stdout.write('Please add them to your .env file or Render environment variables')
            return
        
        # Create or update Google social app
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            google_app.name = 'Google OAuth'
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()
            self.stdout.write(self.style.SUCCESS('✓ Google OAuth app updated'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Google OAuth app created'))
        
        # Add site to the social app
        google_app.sites.clear()
        google_app.sites.add(site)
        
        self.stdout.write(self.style.SUCCESS('\n✓ Google OAuth configured successfully!'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Make sure you have set up Google Cloud Console')
        self.stdout.write('2. Add authorized redirect URI: https://{}/accounts/google/login/callback/'.format(site.domain))
        self.stdout.write('3. Test login at: https://{}/accounts/login/'.format(site.domain))
