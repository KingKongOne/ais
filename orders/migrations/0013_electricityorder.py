# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-27 23:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0073_auto_20180121_1738'),
        ('orders', '0012_auto_20180127_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricityOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_power', models.IntegerField(default=0)),
                ('number_of_outlets', models.IntegerField(default=0)),
                ('equipment_description', models.CharField(blank=True, max_length=150, null=True)),
                ('exhibitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exhibitors.Exhibitor')),
            ],
        ),
    ]