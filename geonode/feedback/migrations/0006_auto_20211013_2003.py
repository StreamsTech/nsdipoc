# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_auto_20180805_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfeedback',
            name='commenter_name',
            field=models.CharField(help_text='', max_length=200, verbose_name='your name'),
        ),
    ]
