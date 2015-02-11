# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0002_auto_20150206_0828'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='ar_file',
            field=models.CharField(max_length=108, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='query',
            name='qr_file',
            field=models.CharField(max_length=108, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='query',
            name='sr_available',
            field=models.IntegerField(max_length=1024, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='query',
            name='sr_completed',
            field=models.IntegerField(max_length=1024, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='query',
            name='sr_cpu',
            field=models.CommaSeparatedIntegerField(max_length=1024, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='query',
            name='sr_used',
            field=models.IntegerField(max_length=1024, null=True),
            preserve_default=True,
        ),
    ]
