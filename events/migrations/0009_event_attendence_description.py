# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20160922_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attendence_description',
            field=models.TextField(blank=True),
        ),
    ]
