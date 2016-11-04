# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_auto_20161029_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examitem',
            old_name='ExamLibItem',
            new_name='examlibitem',
        ),
        migrations.RenameField(
            model_name='paper',
            old_name='ExamLibItem',
            new_name='examlibitem',
        ),
        migrations.AlterField(
            model_name='examlibitem',
            name='category',
            field=models.CharField(max_length=45, choices=[(b'ip', b'IP'), (b'linux', b'Linux'), (b'lte', b'LTE'), (b'python', b'Python'), (b'robot', b'Robot'), (b'test', b'Test'), (b'log', b'LOG')]),
        ),
    ]
