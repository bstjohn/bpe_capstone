# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queryBuilder', '0003_remove_query_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='file_name',
            field=models.CharField(default='n/a', max_length=108),
            preserve_default=True,
        ),
    ]
