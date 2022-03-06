# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop_training', '0003_workshopday_workshopdocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshoptraining',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
