# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-16 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0014_auto_20181015_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='explain',
            field=models.TextField(blank=True, default=b'', max_length=300, null=True),
        ),
    ]
