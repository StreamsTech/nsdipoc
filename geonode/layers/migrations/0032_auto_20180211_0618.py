# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0031_auto_20180102_0200'),
    ]

    operations = [
        migrations.CreateModel(
            name='LayerVersionModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(null=True, blank=True)),
                ('version_path', models.CharField(max_length=500, null=True, blank=True)),
                ('version_name', models.CharField(max_length=400, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='attribute',
            name='is_permitted',
            field=models.NullBooleanField(default=False, help_text='if true, permitted groups will see this attribute', verbose_name='is permitted'),
        ),
        migrations.AddField(
            model_name='layer',
            name='current_version',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='layer',
            name='download_count',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='layer',
            name='file_size',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='layer',
            name='file_type',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='layer',
            name='latest_version',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='layerversionmodel',
            name='layer',
            field=models.ForeignKey(blank=True, to='layers.Layer', null=True),
        ),
    ]
