# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_auto_20161023_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examitem',
            name='answer',
            field=models.TextField(default=b'', max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='examitem',
            name='exam_result',
            field=models.ForeignKey(default=None, blank=True, to='exam.ExamResult', null=True),
        ),
        migrations.AlterField(
            model_name='examitem',
            name='score_result',
            field=models.PositiveIntegerField(default=1, blank=True),
        ),
    ]
