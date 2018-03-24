# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-10 17:50
from __future__ import unicode_literals

from django.db import migrations, models
import fair.models


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0007_auto_20180110_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fair',
            name='description',
            field=models.TextField(default=fair.models.default_name, max_length=500),
        ),
        migrations.AlterField(
            model_name='fair',
            name='name',
            field=models.CharField(default=fair.models.default_name, max_length=100),
        ),
    ]