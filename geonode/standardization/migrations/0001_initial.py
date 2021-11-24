# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0028_auto_20180612_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataProductSpecification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField()),
                ('version', models.CharField(max_length=20, null=True, blank=True)),
                ('remarks', models.TextField(max_length=300, null=True, blank=True)),
                ('doc_file', models.FileField(upload_to=b'dps_files')),
                ('is_active', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DPSDocumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='dataproductspecification',
            name='document_type',
            field=models.ForeignKey(related_name='dps', to='standardization.DPSDocumentType'),
        ),
        migrations.AddField(
            model_name='dataproductspecification',
            name='organization',
            field=models.ForeignKey(related_name='dps', to='groups.GroupProfile'),
        ),
        migrations.AddField(
            model_name='dataproductspecification',
            name='user',
            field=models.ForeignKey(related_name='dps', to=settings.AUTH_USER_MODEL),
        ),
    ]
