# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snaapi', '0006_auto_20161029_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weddingpicture',
            name='thumbnail',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=b'weddingpictures/thumbs/%Y/%m/%d/'),
        ),
    ]
