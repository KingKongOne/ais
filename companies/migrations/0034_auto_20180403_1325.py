# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-03 11:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
        ('companies', '0033_auto_20180403_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['parent', 'name'], 'verbose_name_plural': 'Groups'},
        ),
        migrations.AddField(
            model_name='product',
            name='group',
            field=models.ManyToManyField(to='companies.Group'),
        ),
        migrations.AddField(
            model_name='product',
            name='revenue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Revenue'),
        ),
    ]
