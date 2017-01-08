# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentence', models.TextField(null=True, blank=True)),
                ('book', models.CharField(max_length=120, choices=[(b'nce3', b'NCE3'), (b'nce4', b'NCE4'), (b'bbc', b'BBC'), (b'voa', b'VOA'), (b'cctvnews', b'CCTVNEWS'), (b'mail', b'MAIL'), (b'20000', b'20000'), (b'22000', b'22000')])),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('etymon', models.CharField(max_length=45)),
                ('relation', models.CharField(max_length=120, choices=[(b'synonym', b'Synonym'), (b'antonym', b'Antonym'), (b'homograph', b'Homograph'), (b'etymon', b'etymon')])),
                ('exampleWord', models.ForeignKey(to='engdict.ExampleWord')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('phonetic', models.CharField(max_length=45)),
                ('progress', models.DecimalField(max_digits=50, decimal_places=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('members', models.ManyToManyField(to='engdict.Word', through='engdict.Membership')),
            ],
        ),
        migrations.CreateModel(
            name='WordDict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('explain', models.TextField(null=True, blank=True)),
                ('book', models.CharField(max_length=120, choices=[(b'youdao', b'YOUDAO')])),
                ('word', models.ForeignKey(to='engdict.Word')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='word',
            field=models.ForeignKey(to='engdict.Word'),
        ),
        migrations.AddField(
            model_name='exampleword',
            name='word',
            field=models.ForeignKey(to='engdict.Word'),
        ),
    ]
