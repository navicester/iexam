# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_auto_20161023_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examlibitem',
            name='category',
            field=models.CharField(default='', max_length=45, choices=[(b'ip', b'IP'), (b'lte', b'LTE'), (b'python', b'Python'), (b'robot', b'Robot'), (b'test', b'Test'), (b'log', b'LOG')]),
            preserve_default=False,
        ),
    ]
