from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20241101_1234'),  # ← CHANGE THIS to your actual last migration number/name
        # Example: if your last file is 0012_....py → put '0012_xxxxxx'
    ]

    operations = [
        # These AlterField lines will work even if the columns already exist
        migrations.AlterField(
            model_name='customuser',
            name='otp_code',
            field=models.CharField(max_length=6, blank=True, null=True, default=None, editable=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='otp_created_at',
            field=models.DateTimeField(blank=True, null=True, default=None, editable=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='otp_verified',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]