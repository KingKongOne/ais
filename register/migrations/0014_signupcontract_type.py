# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-29 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0013_auto_20180518_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupcontract',
            name='type',
            field=models.CharField(choices=[('INITIAL', 'Initial'), ('COMPLETE', 'Complete')], default='INITIAL', max_length=200),
            preserve_default=False,
        ),
    ]
