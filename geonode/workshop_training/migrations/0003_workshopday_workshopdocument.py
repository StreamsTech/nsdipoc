# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0028_auto_20180612_1815'),
        ('workshop_training', '0002_auto_20220304_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'GENERAL', max_length=200, choices=[(b'GENERAL', b'General Information'), (b'DAY1', b'Day 1'), (b'DAY2', b'Day 2'), (b'DAY3', b'Day 3'), (b'DAY4', b'Day 4'), (b'DAY5', b'Day 5')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('training_course', models.ForeignKey(related_name='workshop_days', to='workshop_training.WorkshopTraining')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('doc_file', models.FileField(upload_to=b'workshop_training')),
                ('description', models.TextField(max_length=300, null=True, verbose_name=b'Description', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(related_name='documents', to='groups.GroupProfile')),
                ('user', models.ForeignKey(related_name='documents', to=settings.AUTH_USER_MODEL)),
                ('workshop_day', models.ForeignKey(related_name='documents', to='workshop_training.WorkshopTraining')),
            ],
        ),
    ]
