# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-23 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0032_auto_20181023_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitor',
            name='deadline_complete_registration',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Deviating deadline for complete registration'),
        ),
    ]