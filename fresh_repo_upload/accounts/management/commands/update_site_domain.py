from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
import os


class Command(BaseCommand):
    help = 'Updates the Site domain from RENDER_EXTERNAL_HOSTNAME environment variable for Google OAuth'

    def handle(self, *args, **options):
        render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
        
        if render_hostname:
            site = Site.objects.get_current()
            site.domain = render_hostname
            site.name = 'Zambian NRC System'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated site domain to: {render_hostname}'))
        else:
            self.stdout.write(self.style.WARNING('RENDER_EXTERNAL_HOSTNAME not found. Skipping site update.'))
