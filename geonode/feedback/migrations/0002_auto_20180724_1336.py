# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeedback',
            name='contact_no',
            field=models.CharField(blank=True, max_length=17, verbose_name='contact no', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+8801xxxxxxxxx'. Up to 13 digits allowed.")]),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='attachment',
            field=models.FileField(help_text='attatch files or documents if any', upload_to=b'', null=True, verbose_name='attachment', blank=True),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='commenter_name',
            field=models.CharField(default=b'', help_text='', max_length=200, verbose_name='your name'),
        ),
    ]
