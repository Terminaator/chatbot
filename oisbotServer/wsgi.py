"""
WSGI config for oisbotServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

path = '/var/www/chatbot2/chatbot/'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oisbotServer.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
