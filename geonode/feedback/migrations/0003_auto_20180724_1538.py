# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20180724_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfeedback',
            name='commenter_name',
            field=models.CharField(default=b'', help_text='', max_length=200, verbose_name='your name'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='message',
            field=models.TextField(help_text='write your feedback here', max_length=500, verbose_name='message'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='title',
            field=models.CharField(help_text='give a title of your feedback', max_length=50, verbose_name='title'),
        ),
    ]
