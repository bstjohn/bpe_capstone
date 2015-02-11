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
<<<<<<< HEAD
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
>>>>>>> 2d248f6005e2915313680a325146e25732b2ac5f
                ('register_code', models.CharField(max_length=24)),
                ('username', models.CharField(max_length=24)),
                ('email', models.EmailField(max_length=100)),
                ('first_name', models.CharField(max_length=24)),
                ('last_name', models.CharField(max_length=24)),
<<<<<<< HEAD
                ('create_date', models.DateTimeField(auto_now=True, verbose_name=b'create_date')),
            ],
            options=None,
            bases=None,
            managers=None,
=======
                ('create_date', models.DateTimeField(verbose_name='create_date', auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
>>>>>>> 2d248f6005e2915313680a325146e25732b2ac5f
        ),
    ]
