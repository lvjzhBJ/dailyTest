# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-21 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pageGet', '0007_auto_20180121_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsepjt',
            name='add_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6dfb\u52a0\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='responsepjt',
            name='mod_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u66f4\u65b0\u65e5\u671f'),
        ),
    ]
