# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0010_auto_20220304_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfeedback',
            name='commenter_name',
            field=models.CharField(help_text='', max_length=200, verbose_name='your name'),
        ),
    ]
