# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exampleword',
            name='explain',
            field=models.CharField(default=b'', max_length=120),
        ),
        migrations.AddField(
            model_name='word',
            name='explain',
            field=models.TextField(default=b'', max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='progress',
            field=models.DecimalField(default=0, max_digits=50, decimal_places=0),
        ),
    ]
