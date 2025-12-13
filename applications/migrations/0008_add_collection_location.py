# Generated migration for collection location fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_nrcapplication_replacement_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='nrcapplication',
            name='collection_province',
            field=models.CharField(max_length=100, blank=True, null=True, help_text='Province where you want to collect your NRC'),
        ),
        migrations.AddField(
            model_name='nrcapplication',
            name='collection_station',
            field=models.CharField(max_length=200, blank=True, null=True, help_text='Registration office/station for NRC collection'),
        ),
    ]