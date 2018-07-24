# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20180724_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfeedback',
            name='commenter_name',
            field=models.CharField(help_text='', max_length=200, verbose_name='your name'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='contact_no',
            field=models.CharField(max_length=17, verbose_name='phone', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+8801xxxxxxxxx'. Up to 13 digits allowed.")]),
        ),
    ]
