# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('registration', '0002_person_registration_code_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='email_addr_text',
            new_name='email_addr',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='first_name_text',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='last_name_text',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='registration_code_text',
            new_name='registration_code',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='user_name_text',
            new_name='user_name',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='user_password_text',
            new_name='user_password',
        ),
    ]
