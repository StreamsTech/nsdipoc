# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standardization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataproductspecification',
            name='document_type',
            field=models.ForeignKey(related_name='dps', verbose_name=b'Type of document', to='standardization.DPSDocumentType'),
        ),
    ]
