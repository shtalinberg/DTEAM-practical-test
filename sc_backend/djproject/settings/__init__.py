import sys

try:
    from .local import *
except ImportError:
    sys.stderr.write("Unable to read djproject.settings.local.py\n")
    DEBUG = False
