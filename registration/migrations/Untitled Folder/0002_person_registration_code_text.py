# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='registration_code_text',
            field=models.CharField(default=datetime.datetime(2015, 1, 18, 22, 38, 53, 606608, tzinfo=utc), max_length=24),
            preserve_default=False,
        ),
    ]
