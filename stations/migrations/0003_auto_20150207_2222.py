# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0002_auto_20150207_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signal',
            name='id',
        ),
        migrations.AlterField(
            model_name='signal',
            name='Signal_ID',
            field=models.CharField(max_length=200, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
