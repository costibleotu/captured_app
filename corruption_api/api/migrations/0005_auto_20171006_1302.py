# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20171006_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='anb_type',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='ca_criterion',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='ca_procedure',
            field=models.CharField(max_length=50, null=True),
        ),
    ]