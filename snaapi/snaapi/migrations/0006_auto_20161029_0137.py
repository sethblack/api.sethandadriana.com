# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 01:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snaapi', '0005_auto_20161023_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weddingpicture',
            name='thumbnail',
            field=models.ImageField(upload_to=b'weddingpictures/thumbs/%Y/%m/%d/'),
        ),
    ]
