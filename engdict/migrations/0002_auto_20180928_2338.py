# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-28 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exampleword',
            name='book',
            field=models.CharField(choices=[(b'nce3', b'NCE3'), (b'nce4', b'NCE4'), (b'bbc', b'BBC'), (b'voa', b'VOA'), (b'cctvnews', b'CCTVNEWS'), (b'mail', b'MAIL'), (b'20000', b'20000'), (b'22000', b'22000'), (b'100days', b'100days'), (b'YOUDAO', b'YOUDAO')], max_length=120),
        ),
        migrations.AlterField(
            model_name='wordexp',
            name='book',
            field=models.CharField(choices=[(b'nce3', b'NCE3'), (b'nce4', b'NCE4'), (b'bbc', b'BBC'), (b'voa', b'VOA'), (b'cctvnews', b'CCTVNEWS'), (b'mail', b'MAIL'), (b'20000', b'20000'), (b'22000', b'22000'), (b'100days', b'100days'), (b'YOUDAO', b'YOUDAO')], max_length=120),
        ),
    ]
