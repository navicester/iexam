# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-14 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0009_auto_20181013_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='slug',
            field=models.SlugField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='word',
            name='name',
            field=models.CharField(max_length=45, unique=True),
        ),
    ]
