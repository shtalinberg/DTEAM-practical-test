from django.conf import settings


def settings_context(request):
    """
    Context processor that injects Django settings into all templates.
    """
    return {
        'settings': {
            'DEBUG': settings.DEBUG,
            'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
            'TIME_ZONE': settings.TIME_ZONE,
            'USE_TZ': settings.USE_TZ,
            'INSTALLED_APPS': settings.INSTALLED_APPS,
            'MIDDLEWARE': settings.MIDDLEWARE,
        },
    }
