# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-21 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pageGet', '0014_auto_20180121_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='create_time',
            field=models.DurationField(default=1516545560.053357),
        ),
    ]
