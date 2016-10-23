# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_auto_20161023_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examresult',
            name='paper_id',
        ),
        migrations.AddField(
            model_name='examresult',
            name='paper',
            field=models.ForeignKey(default=1, to='exam.Paper'),
            preserve_default=False,
        ),
    ]
