# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_auto_20150223_2257'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
    ]
