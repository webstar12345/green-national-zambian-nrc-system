# New OTP fields migration
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_otp_code_customuser_otp_created_at_and_more'),
    ]

    operations = [
        # These operations are safe and will work even if fields exist
        migrations.AlterField(
            model_name='customuser',
            name='otp_code',
            field=models.CharField(max_length=6, blank=True, null=True, default=None, editable=False, verbose_name="OTP Code"),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='otp_created_at',
            field=models.DateTimeField(blank=True, null=True, default=None, editable=False, verbose_name="OTP Created At"),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='otp_verified',
            field=models.BooleanField(default=False, editable=False, verbose_name="OTP Verified"),
        ),
    ]