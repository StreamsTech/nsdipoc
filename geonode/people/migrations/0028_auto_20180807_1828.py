# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0027_profile_contact_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contact_no',
            field=models.CharField(default=b'None', max_length=17, verbose_name='contact no', blank=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+8801xxxxxxxxx'. Up to 14 digits allowed.")]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_working_group_admin',
            field=models.BooleanField(default=False, help_text='User must be an organization admin tobe committee member', verbose_name='committee member'),
        ),
    ]
