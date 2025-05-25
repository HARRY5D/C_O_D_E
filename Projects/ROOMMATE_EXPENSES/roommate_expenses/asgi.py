"""
ASGI config for roommate_expenses project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roommate_expenses.settings')

application = get_asgi_application()