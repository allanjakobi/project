# Generated by Django 5.1.1 on 2024-11-18 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_agreements_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=128, unique=True)),
                ('reference_number', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='EUR', max_length=3)),
                ('payer_name', models.CharField(max_length=256)),
                ('payer_account', models.CharField(max_length=34)),
                ('payment_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('processed', 'Processed'), ('pending', 'Pending'), ('failed', 'Failed')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
