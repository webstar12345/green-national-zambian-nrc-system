from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from decouple import config


class Command(BaseCommand):
    help = 'Creates a default admin user if one does not exist'

    def handle(self, *args, **options):
        # Get admin credentials from environment variables
        admin_username = config('ADMIN_USERNAME', default='admin')
        admin_email = config('ADMIN_EMAIL', default='admin@nrc.gov.zm')
        admin_password = config('ADMIN_PASSWORD', default='ChangeMe123!')
        
        # Check if admin already exists
        if CustomUser.objects.filter(username=admin_username).exists():
            self.stdout.write(self.style.WARNING(f'Admin user "{admin_username}" already exists'))
            return
        
        # Create admin user
        admin = CustomUser.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            first_name='System',
            last_name='Administrator',
            nrc_number='000000/00/0',
            phone_number='+260000000000'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {admin_username}'))
        self.stdout.write(self.style.WARNING('IMPORTANT: Change the default password immediately!'))
