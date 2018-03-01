# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0033_remove_layer_file_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='file_size',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
    ]
