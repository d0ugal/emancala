import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'pycala.web.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

sys.path.append('/usr/local/django')