# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-01-25 04:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledgerpay', '0005_auto_20210125_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentitem',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='paymentitem',
            name='api_url',
            field=models.URLField(blank=True, verbose_name='API URL'),
        ),
        migrations.AlterField(
            model_name='paymentitem',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='paymentitem',
            name='display_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
