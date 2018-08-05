# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_auto_20180724_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfeedback',
            name='commenter_name',
            field=models.CharField(help_text='', max_length=200, verbose_name='your name'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='message',
            field=models.TextField(help_text='write your feedback here', max_length=5000, verbose_name='message'),
        ),
    ]
