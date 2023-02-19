import os
import ast

DEBUG = os.environ.get('DEBUG', False) == 'True'

if DEBUG:

    INSTALLED_APPS += [
        'debug_toolbar',
        'django_extensions',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INTERNAL_IPS = ast.literal_eval(os.environ.get('INTERNAL_IPS'))
