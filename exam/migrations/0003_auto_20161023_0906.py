# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0002_auto_20161022_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='examitem',
            name='paper',
            field=models.ForeignKey(default=1, to='exam.Paper'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examitem',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='examlibitem',
            name='a',
            field=models.TextField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='examlibitem',
            name='b',
            field=models.TextField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='examlibitem',
            name='c',
            field=models.TextField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='examlibitem',
            name='d',
            field=models.TextField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='examlibitem',
            name='score',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
