# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_delete_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('register_code', models.CharField(max_length=24)),
                ('username', models.CharField(max_length=24)),
                ('email', models.EmailField(unique=True, max_length=100)),
                ('first_name', models.CharField(max_length=24)),
                ('last_name', models.CharField(max_length=24)),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name=b'create_date')),
            ],
            options=None,
            bases=None,
            managers=None,
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='company',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
