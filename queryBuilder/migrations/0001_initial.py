# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('user_name', models.CharField(max_length=24)),
                ('create_date_time', models.DateTimeField(verbose_name='date created')),
                ('query_name', models.CharField(max_length=100)),
                ('start_date_time', models.DateTimeField(verbose_name='query start date time')),
                ('end_date_time', models.DateTimeField(verbose_name='query end date time')),
                ('stations', models.CharField(max_length=1024)),
                ('conditions', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
