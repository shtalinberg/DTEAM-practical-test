from django.contrib import admin

from audit.models import RequestLog

# Register your models here.


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    """Admin interface for RequestLog model."""

    list_display = (
        'timestamp',
        'method',
        'path',
        'remote_ip',
        'user',
        'response_status',
        'response_time_ms',
    )
    search_fields = ('path', 'remote_ip')
    list_filter = ('method', 'response_status')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
