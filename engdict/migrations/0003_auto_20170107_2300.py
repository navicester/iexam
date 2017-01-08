# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0002_auto_20161120_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordExp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phonetic', models.CharField(max_length=45)),
                ('explain', models.CharField(default=b'', max_length=120)),
                ('sentence', models.TextField(null=True, blank=True)),
                ('book', models.CharField(max_length=120, choices=[(b'nce3', b'NCE3'), (b'nce4', b'NCE4'), (b'bbc', b'BBC'), (b'voa', b'VOA'), (b'cctvnews', b'CCTVNEWS'), (b'mail', b'MAIL'), (b'20000', b'20000'), (b'22000', b'22000')])),
            ],
        ),
        migrations.AddField(
            model_name='word',
            name='exp',
            field=models.ManyToManyField(to='engdict.WordExp'),
        ),
    ]
