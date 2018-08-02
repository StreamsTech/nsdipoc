# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20180730_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datacatalog',
            name='fromat',
        ),
        migrations.AddField(
            model_name='datacatalog',
            name='format',
            field=models.CharField(help_text='', max_length=300, verbose_name='', blank=True),
        ),
    ]
