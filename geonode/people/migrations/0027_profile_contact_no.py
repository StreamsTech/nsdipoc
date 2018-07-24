# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0026_auto_20180211_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contact_no',
            field=models.CharField(blank=True, max_length=17, verbose_name='contact no', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+8801xxxxxxxxx'. Up to 13 digits allowed.")]),
        ),
    ]
