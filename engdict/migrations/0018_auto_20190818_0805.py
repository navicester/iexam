# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-08-18 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0017_auto_20181017_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='worddict',
            name='phonetic',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='worddict',
            name='book',
            field=models.CharField(choices=[(b'youdao', b'YOUDAO'), (b'kingsoft', b'kingsoft'), (b'nce3', b'nce3'), (b'nce4', b'nce4')], default=b'youdao', max_length=120),
        ),
    ]
