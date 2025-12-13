# Fresh OTP Migration - No Cache Conflicts 
from django.db import migrations, models 
 
 
class Migration(migrations.Migration): 
 
    dependencies = [ 
        ('accounts', '0003_customuser_otp_code_customuser_otp_created_at_and_more'), 
    ] 
 
    operations = [ 
        # No-op migration - fields already exist from 0003 
        # This just ensures the migration chain is complete 
    ] 
