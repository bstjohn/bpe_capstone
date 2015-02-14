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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('register_code', models.CharField(max_length=24)),
                ('username', models.CharField(max_length=24)),
                ('email', models.EmailField(max_length=100)),
                ('first_name', models.CharField(max_length=24)),
                ('last_name', models.CharField(max_length=24)),
                ('create_date', models.DateTimeField(verbose_name='create_date', auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
