# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_auto_20180604_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcebase',
            name='thumbnail_url',
            field=models.TextField(help_text='Thumbnail url for this layer. You can change this if you want to use custom thumbnail', null=True, blank=True),
        ),
    ]
