# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_auto_20161023_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='score',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
