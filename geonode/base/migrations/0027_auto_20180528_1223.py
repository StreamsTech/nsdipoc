# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_auto_20180528_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcebase',
            name='status',
            field=models.CharField(default=b'DRAFT', max_length=10, choices=[(b'DRAFT', 'Draft'), (b'PENDING', 'Pending'), (b'ACTIVE', 'Active'), (b'INACTIVE', 'Inactive'), (b'DENIED', 'Denied'), (b'DELETED', 'Deleted'), (b'CANCELED', 'Canceled')]),
        ),
    ]
