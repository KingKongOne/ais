# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-07 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0043_auto_20181105_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitor',
            name='checked_in',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date and time of check in'),
        ),
    ]
