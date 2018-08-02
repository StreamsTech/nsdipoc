# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datacatalog',
            name='inside_org',
            field=models.CharField(help_text='inside the organization only', max_length=300, verbose_name='inside the organization', blank=True),
        ),
        migrations.AlterField(
            model_name='datacatalog',
            name='fromat',
            field=models.CharField(help_text='', max_length=300, verbose_name='', blank=True),
        ),
    ]
