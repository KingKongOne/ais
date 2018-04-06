# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-06 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0081_remove_exhibitor_invoice_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibitor',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyContact'),
        ),
    ]
