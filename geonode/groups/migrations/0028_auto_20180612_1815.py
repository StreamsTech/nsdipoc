# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0027_auto_20180612_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='department',
            field=models.ForeignKey(related_name='organizations', verbose_name=b'Type', to='nsdi.DepartmentModel', null=True),
        ),
    ]
