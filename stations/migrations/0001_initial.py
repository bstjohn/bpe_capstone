# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Signal_ID', models.IntegerField(default=-1)),
                ('Signal_Index', models.IntegerField(default=-1)),
                ('Signal_Name_Raw', models.CharField(max_length=200)),
                ('Signal_Name_Short', models.CharField(max_length=200)),
                ('Signal_Name_Group', models.CharField(max_length=200)),
                ('Signal_Name_Long', models.CharField(max_length=200)),
                ('Signal_Type', models.CharField(max_length=200)),
                ('Signal_Asset', models.CharField(max_length=200)),
                ('Signal_Voltage', models.IntegerField(default=-1)),
                ('Signal_Circuit', models.IntegerField(default=-1)),
                ('Signal_Unit', models.CharField(max_length=200)),
                ('Signal_Phase', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PMU_ID', models.IntegerField(default=-1)),
                ('PMU_Company', models.CharField(max_length=200)),
                ('PMU_Name_Raw', models.CharField(max_length=200)),
                ('PMU_Name_Short', models.CharField(max_length=200)),
                ('PMU_Name_Long', models.CharField(max_length=200)),
                ('PMU_Set', models.IntegerField(default=-1)),
                ('PMU_Channel', models.CharField(max_length=1)),
                ('PMU_Type', models.CharField(max_length=5)),
                ('PMU_Voltage', models.IntegerField(default=-1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='signal',
            name='Signal_PMU_ID',
            field=models.ForeignKey(to='stations.Station'),
            preserve_default=True,
        ),
    ]
