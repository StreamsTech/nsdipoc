# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_training', '0004_auto_20220304_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopdocument',
            name='workshop_day',
            field=models.ForeignKey(related_name='documents', to='workshop_training.WorkshopDay'),
        ),
    ]
