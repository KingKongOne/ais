# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-03 15:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0081_remove_exhibitor_invoice_details'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0039_companylog_fair'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCustomerResponsible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Company customers',
                'ordering': ['company__name'],
            },
        ),
        migrations.RemoveField(
            model_name='invoicedetails',
            name='company',
        ),
        migrations.AlterModelOptions(
            name='companyaddress',
            options={'ordering': ['company__name'], 'verbose_name_plural': 'Company addresses'},
        ),
        migrations.AlterModelOptions(
            name='companycustomer',
            options={'ordering': ['company__name'], 'verbose_name_plural': 'Company customers'},
        ),
        migrations.RenameField(
            model_name='company',
            old_name='organisation_number',
            new_name='identity_number',
        ),
        migrations.RemoveField(
            model_name='company',
            name='related_programme',
        ),
        migrations.AddField(
            model_name='companylog',
            name='action',
            field=models.CharField(choices=[('create', 'Company created')], default='create', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companylog',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='InvoiceDetails',
        ),
        migrations.AddField(
            model_name='companycustomerresponsible',
            name='company_customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyCustomer'),
        ),
        migrations.AddField(
            model_name='companycustomerresponsible',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Group'),
        ),
        migrations.AddField(
            model_name='companycustomerresponsible',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]