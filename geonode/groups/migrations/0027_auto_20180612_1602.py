# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0026_auto_20180211_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='department',
            field=models.ForeignKey(related_name='organizations', to='nsdi.DepartmentModel', null=True),
        ),
    ]
