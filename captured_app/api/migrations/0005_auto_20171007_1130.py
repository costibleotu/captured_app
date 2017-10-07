# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_contract_market'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('short', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='contract',
            name='country',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.Country'),
            preserve_default=False,
        ),
    ]