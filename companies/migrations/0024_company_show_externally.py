# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-17 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0023_merge_20181004_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='show_externally',
            field=models.BooleanField(default=True),
        ),
    ]