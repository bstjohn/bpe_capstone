# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20150224_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='company',
            field=models.CharField(max_length=24, null=True),
            preserve_default=True,
        ),
    ]
