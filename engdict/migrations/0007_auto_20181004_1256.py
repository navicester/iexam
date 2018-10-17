# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-04 04:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engdict', '0006_word_linked_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordexp',
            name='word',
            field=models.ManyToManyField(blank=True, related_name='wordexp', to='engdict.Word'),
        ),
    ]