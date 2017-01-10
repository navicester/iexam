# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0008_remove_word_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordexp',
            name='etymon',
            field=models.CharField(max_length=45, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wordexp',
            name='name',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordexp',
            name='relation',
            field=models.CharField(default=b'Self', max_length=120, choices=[(b'Self', b'Self'), (b'synonym', b'Synonym'), (b'antonym', b'Antonym'), (b'homograph', b'Homograph'), (b'etymon', b'etymon')]),
        ),
        migrations.AlterField(
            model_name='membership',
            name='relation',
            field=models.CharField(max_length=120, choices=[(b'Self', b'Self'), (b'synonym', b'Synonym'), (b'antonym', b'Antonym'), (b'homograph', b'Homograph'), (b'etymon', b'etymon')]),
        ),
    ]
