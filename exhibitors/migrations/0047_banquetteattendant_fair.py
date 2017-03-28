# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-18 21:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0003_auto_20170218_2244'),
        ('exhibitors', '0046_exhibitor_manual_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='banquetteattendant',
            name='fair',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fair.Fair'),
        ),
    ]