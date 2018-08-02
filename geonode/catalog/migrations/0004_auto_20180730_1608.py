# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0028_auto_20180612_1815'),
        ('catalog', '0003_auto_20180730_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='datacatalog',
            name='ownership',
            field=models.ForeignKey(blank=True, to='groups.GroupProfile', help_text='the organization that owns this catalog', null=True, verbose_name='owner ship'),
        ),
        migrations.AlterField(
            model_name='datacatalog',
            name='format',
            field=models.CharField(help_text='type of data, it may Shape, image, pdf etc.', max_length=300, verbose_name='format of data', blank=True),
        ),
    ]
