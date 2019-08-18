# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-08-18 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0019_auto_20190818_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
