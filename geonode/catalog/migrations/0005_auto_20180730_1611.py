# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20180730_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datacatalog',
            name='ownership',
            field=models.ForeignKey(verbose_name='owner ship', to='groups.GroupProfile', help_text='the organization that owns this catalog'),
        ),
    ]
