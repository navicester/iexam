# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0007_auto_20170108_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='members',
        ),
    ]
