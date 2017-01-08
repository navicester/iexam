# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0003_auto_20170107_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='exp',
        ),
        migrations.AddField(
            model_name='wordexp',
            name='exp',
            field=models.ManyToManyField(to='engdict.WordExp'),
        ),
    ]
