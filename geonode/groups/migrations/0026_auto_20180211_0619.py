# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nsdi', '0001_initial'),
        ('groups', '0025_auto_20171004_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=50)),
                ('slug', models.SlugField(max_length=100, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='department',
            field=models.ForeignKey(related_name='department', to='nsdi.DepartmentModel', null=True),
        ),
        migrations.AddField(
            model_name='sectionmodel',
            name='organization',
            field=models.ForeignKey(related_name='groupprofile', blank=True, to='groups.GroupProfile', null=True),
        ),
    ]
