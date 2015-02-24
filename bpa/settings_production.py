# settings_production.py

from settings import *

DEBUG = TEMPLATE_DEBUG = True
DATABASE_NAME = 'bpa_production'
DATABASE_USER = 'bpa'
DATABASE_PASSWORD = 'bpa'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'bpa',
            'USER': 'bpa',
            'PASSWORD': 'bpa',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            }
        }
