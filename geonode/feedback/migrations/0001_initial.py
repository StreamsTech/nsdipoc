# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', help_text='give a title of your feedback', max_length=50, verbose_name='title')),
                ('commenter_name', models.CharField(default=b'', help_text='', max_length=200, verbose_name='your name')),
                ('commenter_email', models.EmailField(help_text='your email', max_length=254, verbose_name='email')),
                ('message', models.TextField(default=b'', help_text='write your feedback here', max_length=500, verbose_name='message')),
                ('slug', models.SlugField(max_length=100, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('attachment', models.FileField(upload_to=b'', null=True, verbose_name='attachment', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
