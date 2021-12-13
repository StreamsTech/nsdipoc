# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_auto_20180726_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcebase',
            name='title',
            field=models.CharField(help_text='name by which the cited resource is known', max_length=255, verbose_name='Title'),
        ),
    ]
