# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-29 11:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0023_merge_20181004_0954'),
        ('fair', '0004_auto_20181003_1227'),
        ('unirel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='unirel_participant_company', to='companies.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='fair',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fair.Fair'),
            preserve_default=False,
        ),
    ]
