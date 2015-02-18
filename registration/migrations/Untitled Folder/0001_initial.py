# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name_text', models.CharField(max_length=24)),
                ('last_name_text', models.CharField(max_length=24)),
                ('user_name_text', models.CharField(max_length=24)),
                ('user_password_text', models.CharField(max_length=24)),
                ('email_addr_text', models.CharField(max_length=100)),
                ('create_date', models.DateTimeField(verbose_name=b'date created')),
            ],
            options=None,
            bases=None,
            managers=None,
        ),
    ]
