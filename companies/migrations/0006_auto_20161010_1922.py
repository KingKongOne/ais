# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_auto_20161006_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='company',
            name='organisation_number',
            field=models.CharField(max_length=100),
        ),
    ]