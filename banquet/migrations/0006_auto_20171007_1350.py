# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-07 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0006_auto_20170831_2211'),
        ('banquet', '0005_banquetteattendant_ticket_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BanquetTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(blank=True, max_length=20, null=True)),
                ('number_of_seats', models.IntegerField(blank=True, null=True)),
                ('fair', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fair.Fair')),
            ],
            options={
                'ordering': ['table_name'],
            },
        ),
        migrations.RemoveField(
            model_name='banquetteattendant',
            name='table_name',
        ),
        migrations.AddField(
            model_name='banquetteattendant',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='banquet.BanquetTable'),
        ),
    ]
