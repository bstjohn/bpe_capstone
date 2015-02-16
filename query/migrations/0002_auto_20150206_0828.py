# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('query', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='signal_circuit_number',
        ),
        migrations.RemoveField(
            model_name='query',
            name='signal_measurement',
        ),
        migrations.RemoveField(
            model_name='query',
            name='signal_measurement_identifier',
        ),
        migrations.RemoveField(
            model_name='query',
            name='signal_nominal_volts',
        ),
        migrations.RemoveField(
            model_name='query',
            name='signal_suffix',
        ),
    ]
