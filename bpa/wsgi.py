"""
WSGI config for bpe_capstone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os, sys, site

# add the virtualenv
root = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(root)
site.addsitedir(os.path.join(root, "env/lib/python3.3/site-packages"))
site.addsitedir(os.path.join(root, "env/lib64/python3.3/site-packages"))
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bpa.settings_production")
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
