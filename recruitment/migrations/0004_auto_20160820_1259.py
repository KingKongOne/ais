# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-20 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0003_customfield_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitmentapplication',
            name='interview_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
