# Generated by Django 5.1.1 on 2024-11-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_users_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreements',
            name='extended',
            field=models.IntegerField(default=0),
        ),
    ]
