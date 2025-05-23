import logging
import time

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from audit.models import RequestLog

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log HTTP requests to the database.
    Logs all requests except EXCLUDED_PATHS.
    """

    # Paths to exclude from logging (static files, admin media, etc.)
    EXCLUDED_PATHS = [
        '/static/',
        '/media/',
        '/favicon.ico',
        '/robots.txt',
        '/__debug__/',  # Django Debug Toolbar
    ]

    # Additional exclusions from settings
    EXCLUDED_PATHS += getattr(settings, 'AUDIT_EXCLUDED_PATHS', [])

    def process_request(self, request):
        """Store request start time."""
        request._request_start_time = time.time()

    def process_response(self, request, response):
        """Log the request after processing."""
        # Skip if path should be excluded
        if any(request.path.startswith(excluded) for excluded in self.EXCLUDED_PATHS):
            return response

        # Calculate response time
        response_time_ms = None
        if hasattr(request, '_request_start_time'):
            response_time = (time.time() - request._request_start_time) * 1000
            response_time_ms = int(response_time)

        # Create log entry
        try:
            RequestLog.objects.create(
                method=request.method,
                path=request.path,
                query_string=request.META.get('QUERY_STRING', ''),
                remote_ip=self._get_client_ip(request),
                user=request.user if request.user.is_authenticated else None,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                response_status=response.status_code,
                response_time_ms=response_time_ms,
            )
        except Exception as exc:
            logger.exception("Error logging request: %s", exc)
            if settings.DEBUG:
                print(f"Request logging error: {exc}")

        return response

    def _get_client_ip(self, request):
        """Get client IP address from request. Simple way"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
