import os
import sys

sys.path.append("/home/jnp/repo/")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jnp3.settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

