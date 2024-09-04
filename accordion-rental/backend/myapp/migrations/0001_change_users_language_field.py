# Generated by Django 5.1 on 2024-09-04 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('modelId', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=64)),
                ('model', models.CharField(max_length=128)),
                ('keys', models.IntegerField()),
                ('low', models.IntegerField()),
                ('sb', models.IntegerField()),
                ('bRows', models.IntegerField()),
                ('fb', models.IntegerField(default=0)),
                ('reedsR', models.IntegerField()),
                ('reedsL', models.IntegerField()),
                ('reeds_fb', models.IntegerField(default=0)),
                ('range_fb', models.IntegerField(default=0)),
                ('fb_low', models.IntegerField(default=0)),
                ('regR', models.IntegerField()),
                ('regL', models.IntegerField()),
                ('height', models.FloatField(default=36)),
                ('width', models.FloatField(default=18)),
                ('weight', models.FloatField()),
                ('keyboard', models.FloatField()),
                ('newPrice', models.FloatField(default=2000)),
                ('usedPrice', models.FloatField(default=1000)),
            ],
            options={
                'db_table': 'model',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Agreements',
            fields=[
                ('agreementId', models.AutoField(primary_key=True, serialize=False)),
                ('referenceNr', models.IntegerField(default=1, editable=False, unique=True)),
                ('startDate', models.DateField()),
                ('months', models.IntegerField(default=12)),
                ('rate', models.IntegerField(editable=False)),
                ('status', models.CharField(default='Created', editable=False, max_length=128)),
                ('invoice_interval', models.IntegerField(default=1)),
                ('info', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'agreements',
            },
        ),
        migrations.CreateModel(
            name='Rates',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rateId', models.IntegerField()),
                ('description', models.CharField(max_length=256)),
                ('rate', models.FloatField()),
                ('startDate', models.DateField()),
            ],
            options={
                'db_table': 'rates',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('userId', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=128)),
                ('lastName', models.CharField(max_length=128)),
                ('country', models.CharField(default='Estonia', max_length=128)),
                ('province', models.CharField(max_length=128)),
                ('municipality', models.CharField(max_length=128)),
                ('settlement', models.CharField(max_length=128)),
                ('street', models.CharField(max_length=128)),
                ('house', models.CharField(max_length=128)),
                ('apartment', models.CharField(blank=True, max_length=128, null=True)),
                ('phone', models.CharField(default='+372', max_length=128)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('institution', models.CharField(blank=True, max_length=128, null=True)),
                ('teacher', models.CharField(blank=True, max_length=128, null=True)),
                ('language', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('status', models.TextField()),
                ('agreementId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.agreements')),
            ],
            options={
                'db_table': 'invoices',
            },
        ),
        migrations.CreateModel(
            name='Rendipillid',
            fields=[
                ('instrumentId', models.AutoField(primary_key=True, serialize=False)),
                ('color', models.CharField(max_length=64)),
                ('serial', models.CharField(max_length=64)),
                ('info_est', models.TextField()),
                ('info_eng', models.TextField()),
                ('status', models.CharField(max_length=64)),
                ('price_level', models.IntegerField(default=1)),
                ('modelId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.model')),
            ],
            options={
                'db_table': 'rendipillid',
            },
        ),
        migrations.AddField(
            model_name='agreements',
            name='instrumentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.rendipillid'),
        ),
        migrations.AddField(
            model_name='agreements',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.users'),
        ),
    ]