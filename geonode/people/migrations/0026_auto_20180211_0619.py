# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0026_auto_20180211_0619'),
        ('people', '0025_profile_last_notification_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_working_group_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='section',
            field=models.ForeignKey(related_name='section', to='groups.SectionModel', null=True),
        ),
    ]
