# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snaapi', '0002_auto_20161023_0426'),
    ]

    operations = [
        migrations.AddField(
            model_name='weddingpicture',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
