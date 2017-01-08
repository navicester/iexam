# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0005_remove_wordexp_exp'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordexp',
            name='word',
            field=models.ManyToManyField(to='engdict.Word'),
        ),
    ]
