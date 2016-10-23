# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField(max_length=500, verbose_name=b'answer')),
                ('score_result', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ExamLibItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(max_length=500)),
                ('a', models.TextField(max_length=500)),
                ('b', models.TextField(max_length=500)),
                ('c', models.TextField(max_length=500)),
                ('d', models.TextField(max_length=500)),
                ('score', models.PositiveIntegerField(null=True, blank=True)),
                ('ref_answer', models.TextField(max_length=500, verbose_name=b'ref_answer')),
                ('category', models.CharField(max_length=45, null=True, blank=True)),
                ('source', models.CharField(max_length=120, null=True, blank=True)),
                ('contributor', models.CharField(max_length=45, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExamResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paper_id', models.IntegerField()),
                ('score', models.IntegerField(null=True, blank=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('type', models.CharField(max_length=45, choices=[(b'a', b'A'), (b'b', b'B'), (b'c', b'C'), (b'd', b'D')])),
                ('total_score', models.IntegerField()),
                ('ExamLibItem', models.ManyToManyField(to='exam.ExamLibItem', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='examitem',
            name='ExamLibItem',
            field=models.ForeignKey(to='exam.ExamLibItem'),
        ),
        migrations.AddField(
            model_name='examitem',
            name='exam_result',
            field=models.ForeignKey(to='exam.ExamResult'),
        ),
    ]
