# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('user_name', models.CharField(max_length=24)),
                ('create_date_time', models.DateTimeField(verbose_name='date created')),
                ('query_name', models.CharField(max_length=100)),
                ('start_date_time', models.DateTimeField(verbose_name='query start date time')),
                ('end_date_time', models.DateTimeField(verbose_name='query end date time')),
                ('stations', models.CharField(max_length=1024)),
                ('signal_measurement', models.CharField(max_length=24)),
                ('signal_nominal_volts', models.IntegerField(max_length=3)),
                ('signal_circuit_number', models.IntegerField(max_length=1)),
                ('signal_measurement_identifier', models.CharField(max_length=24)),
                ('signal_suffix', models.CharField(max_length=24)),
                ('conditions', models.CharField(max_length=1024)),
                ('file_name', models.CharField(default='n/a', max_length=108)),
                ('owner', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
