# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('days', models.IntegerField(verbose_name=b'Days')),
                ('date_from', models.DateTimeField(verbose_name=b'Date from')),
                ('date_to', models.DateTimeField(verbose_name=b'To')),
                ('overview', models.TextField(max_length=300, null=True, verbose_name=b'Overview', blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
