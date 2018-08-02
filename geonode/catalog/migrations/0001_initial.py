# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataCatalog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='give a title of your catalog', max_length=300, verbose_name='title')),
                ('fromat', models.CharField(help_text='', max_length=300, verbose_name='', blank=True)),
                ('no_of_layer', models.CharField(help_text='total number of layers', max_length=300, verbose_name='number of layers', blank=True)),
                ('coordinate_system', models.CharField(help_text='the coordinate system of this data', max_length=300, verbose_name='coordinate system', blank=True)),
                ('projection', models.CharField(help_text='projection of data', max_length=300, verbose_name='projection', blank=True)),
                ('dimension', models.CharField(help_text='dimension (2D/3D with height)', max_length=300, verbose_name='dimension (2D/3D)', blank=True)),
                ('display_scale', models.CharField(help_text='suitable scale for dispalay', max_length=300, verbose_name='display scale', blank=True)),
                ('area', models.CharField(help_text='total area covered by the layers', max_length=300, verbose_name='area covered', blank=True)),
                ('preparation_year', models.CharField(help_text='year of preparation/revision', max_length=300, verbose_name='year of preparation', blank=True)),
                ('volume', models.CharField(help_text='volume of data (KB, MB, GB)', max_length=300, verbose_name='volume', blank=True)),
                ('govt_org', models.CharField(help_text='governmental organization only', max_length=300, verbose_name='governmental organization only', blank=True)),
                ('inside_ministy', models.CharField(help_text='inside the ministry only', max_length=300, verbose_name='inside the ministry', blank=True)),
                ('restricted_information', models.CharField(help_text='total restricted information', max_length=300, verbose_name='restricted information', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
