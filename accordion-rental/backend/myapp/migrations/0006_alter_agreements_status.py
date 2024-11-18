# Generated by Django 5.1.1 on 2024-11-17 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_agreements_extended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreements',
            name='status',
            field=models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Test', 'Test'), ('EndingSoon', 'Ending Soon'), ('Ended', 'Ended'), ('Finished', 'Finished')], default='Created', editable=False, max_length=15),
        ),
    ]