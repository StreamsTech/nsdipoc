# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0037_auto_20180726_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='title_en',
            field=models.CharField(help_text='name by which the cited resource is known', max_length=255, null=True, verbose_name='Title'),
        ),
    ]
