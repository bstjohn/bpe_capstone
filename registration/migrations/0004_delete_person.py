# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20150223_2109'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
    ]
