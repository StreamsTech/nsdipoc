# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0034_layer_file_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='is_base_layer',
            field=models.BigIntegerField(default=False),
        ),
    ]
