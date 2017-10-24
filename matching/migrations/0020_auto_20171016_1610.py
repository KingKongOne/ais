# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-16 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0019_auto_20171016_1404'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workfieldarea',
            options={'default_permissions': (), 'verbose_name': 'work field area'},
        ),
        migrations.AddField(
            model_name='studentanswerbase',
            name='created',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='studentanswerbase',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]