# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-06 21:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        #('auth', '0009_group_fair'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(default=-1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')], max_length=1)),
                ('shirt_size', models.CharField(blank=True, choices=[(b'WXS', b'Woman X-Small'), (b'WS', b'Woman Small'), (b'WM', b'Woman Medium'), (b'WL', b'Woman Large'), (b'WXL', b'Woman X-Large'), (b'MXS', b'Man X-Small'), (b'MS', b'Man Small'), (b'MM', b'Man Medium'), (b'ML', b'Man Large'), (b'MXL', b'Man X-Large')], max_length=3)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('drivers_license', models.CharField(blank=True, max_length=10, null=True)),
                ('allergy', models.CharField(blank=True, max_length=30, null=True)),
                ('programme', models.CharField(blank=True, max_length=30, null=True)),
                ('registration_year', models.IntegerField(blank=True, null=True)),
                ('planned_graduation', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
    ]