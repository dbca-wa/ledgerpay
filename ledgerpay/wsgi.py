"""
WSGI config for ledgerpay project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ledgerpay.settings")
#
# application = get_wsgi_application()

"""
WSGI config for ledger project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling
import confy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confy.read_environment_file(BASE_DIR+"/.env")
os.environ.setdefault("BASE_DIR", BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ledgerpay.settings")
#application = get_wsgi_application()
application = Cling(MediaCling(get_wsgi_application()))