# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-21 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pageGet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responsepjt',
            name='create_time',
        ),
        migrations.AddField(
            model_name='responsepjt',
            name='add_time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='responsepjt',
            name='mod_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
