# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0006_wordexp_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordexp',
            name='word',
            field=models.ManyToManyField(to='engdict.Word', null=True, blank=True),
        ),
    ]
