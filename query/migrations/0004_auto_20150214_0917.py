# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0003_auto_20150211_0125'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemCpu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpu_id', models.IntegerField(max_length=1024)),
                ('cpu_load', models.FloatField(default=0, max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SystemNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_id', models.IntegerField(max_length=100)),
                ('used', models.IntegerField(max_length=1024, null=True)),
                ('available', models.IntegerField(max_length=1024, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SystemStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('system_id', models.IntegerField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='systemnode',
            name='system',
            field=models.ForeignKey(to='query.SystemStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='systemcpu',
            name='node',
            field=models.ForeignKey(to='query.SystemNode'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='query',
            name='sr_available',
        ),
        migrations.RemoveField(
            model_name='query',
            name='sr_cpu',
        ),
        migrations.RemoveField(
            model_name='query',
            name='sr_used',
        ),
        migrations.AddField(
            model_name='query',
            name='status_field',
            field=models.CharField(max_length=1024, null=True),
            preserve_default=True,
        ),
    ]
