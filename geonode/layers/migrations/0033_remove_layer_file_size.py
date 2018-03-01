# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0032_auto_20180211_0618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='layer',
            name='file_size',
        ),
    ]
