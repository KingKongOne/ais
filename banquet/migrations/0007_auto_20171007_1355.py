# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-07 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banquet', '0006_auto_20171007_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banquettable',
            name='table_name',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
