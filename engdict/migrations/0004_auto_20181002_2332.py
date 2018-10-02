# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-02 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0003_auto_20181002_1047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='exampleword',
            name='book',
            field=models.CharField(choices=[(b'nce3', b'NCE3'), (b'nce4', b'NCE4'), (b'bbc', b'BBC'), (b'voa', b'VOA'), (b'cctvnews', b'CCTVNEWS'), (b'mail', b'MAIL'), (b'life', b'LIFE'), (b'20000', b'20000'), (b'22000', b'22000'), (b'100days', b'100days'), (b'IELTS', b'IELTS'), (b'BSWX', b'BSWX'), (b'YOUDAO', b'YOUDAO')], max_length=120),
        ),
        migrations.AlterField(
            model_name='word',
            name='phonetic',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='wordexp',
            name='book',
            field=models.CharField(choices=[(b'nce3', b'NCE3'), (b'nce4', b'NCE4'), (b'bbc', b'BBC'), (b'voa', b'VOA'), (b'cctvnews', b'CCTVNEWS'), (b'mail', b'MAIL'), (b'life', b'LIFE'), (b'20000', b'20000'), (b'22000', b'22000'), (b'100days', b'100days'), (b'IELTS', b'IELTS'), (b'BSWX', b'BSWX'), (b'YOUDAO', b'YOUDAO')], max_length=120),
        ),
        migrations.AlterField(
            model_name='wordexp',
            name='phonetic',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
