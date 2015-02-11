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
            name='Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
<<<<<<< HEAD
            options=None,
            bases=None,
            managers=None,
=======
            options={
            },
            bases=(models.Model,),
>>>>>>> 2d248f6005e2915313680a325146e25732b2ac5f
        ),
    ]
