# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examlibitem',
            name='type',
            field=models.CharField(default='Choice', max_length=45, choices=[(b'choice', b'Choice'), (b'answer', b'Answer')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='examitem',
            name='answer',
            field=models.TextField(max_length=500),
        ),
    ]
