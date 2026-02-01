"""
WSGI config for newssite project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newssite.settings')
application = get_wsgi_application()
