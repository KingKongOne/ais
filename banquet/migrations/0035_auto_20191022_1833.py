# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-22 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banquet', '0034_auto_20191022_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afterpartyticket',
            name='email_address',
            field=models.EmailField(max_length=75, verbose_name='E-mail address'),
        ),
        migrations.AlterField(
            model_name='afterpartyticket',
            name='name',
            field=models.CharField(max_length=75),
        ),
    ]
