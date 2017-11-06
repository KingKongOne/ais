# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0006_auto_20170831_2211'),
        ('exhibitors', '0064_exhibitor_location_at_fair'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitor',
            name='tags',
            field=models.ManyToManyField(blank=True, to='fair.Tag'),
        ),
    ]