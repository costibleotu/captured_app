# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_contract_contract_value_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Influence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj_id', models.CharField(max_length=20)),
                ('contracts_no', models.IntegerField()),
                ('bridging_capacity', models.IntegerField()),
                ('influence', models.FloatField()),
            ],
        ),
    ]