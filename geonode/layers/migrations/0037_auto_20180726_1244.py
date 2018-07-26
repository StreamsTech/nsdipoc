# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0036_layer_geometry_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='time_regex',
            field=models.CharField(blank=True, max_length=128, null=True, help_text='regular expression for time. You can use any one of these', choices=[(b'[0-9]{8}', 'YYYYMMDD'), (b'[0-9]{8}T[0-9]{6}', "YYYYMMDD'T'hhmmss"), (b'[0-9]{8}T[0-9]{6}Z', "YYYYMMDD'T'hhmmss'Z'")]),
        ),
    ]
