import os

import dj_database_url

from .base_django import *

DEBUG = False


DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}
