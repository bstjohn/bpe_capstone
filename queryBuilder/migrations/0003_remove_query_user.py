# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queryBuilder', '0002_query_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='user',
        ),
    ]
