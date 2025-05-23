from datetime import timedelta

from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import RequestLog


def recent_requests(request):
    """Display 10 most recent logged requests."""
    recent_logs = RequestLog.objects.select_related('user').order_by('-timestamp')[:10]

    return render(
        request,
        'audit/recent_requests.html',
        {
            'recent_logs': recent_logs,
        },
    )


def log_requests(request):
    """Display recent logged requests."""
    # Get filter parameters
    method_filter = request.GET.get('method', '')
    path_filter = request.GET.get('path', '')
    user_filter = request.GET.get('user', '')
    status_filter = request.GET.get('status', '')

    # Base queryset - get recent requests
    logs = RequestLog.objects.select_related('user').all()

    # Apply filters
    if method_filter:
        logs = logs.filter(method=method_filter)

    if path_filter:
        logs = logs.filter(path__icontains=path_filter)

    if user_filter:
        logs = logs.filter(
            Q(user__username__icontains=user_filter)
            | Q(user__first_name__icontains=user_filter)
            | Q(user__last_name__icontains=user_filter)
        )

    if status_filter:
        try:
            status_code = int(status_filter)
            logs = logs.filter(response_status=status_code)
        except ValueError:
            pass

    # Pagination
    paginator = Paginator(logs, 20)  # Show 20 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get statistics for dashboard
    stats = _get_request_stats()

    # Get values for filters
    unique_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

    ctx = {
        'page_obj': page_obj,
        'stats': stats,
        'unique_methods': unique_methods,
        'filters': {
            'method': method_filter,
            'path': path_filter,
            'user': user_filter,
            'status': status_filter,
        },
    }

    # HTMX support - return partial template for AJAX requests
    if request.headers.get('HX-Request'):
        return render(request, 'audit/partials/logs_table.html', ctx)

    return render(request, 'audit/log_requests.html', ctx)


def request_stats_api(request):
    """API endpoint for request statistics (for HTMX updates)."""
    stats = _get_request_stats()
    return JsonResponse(stats)


def _get_request_stats():
    """Calculate request statistics."""
    now = timezone.now()

    # Time periods
    last_hour = now - timedelta(hours=1)
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)

    # Basic counts
    total_requests = RequestLog.objects.count()
    requests_last_hour = RequestLog.objects.filter(timestamp__gte=last_hour).count()
    requests_last_24h = RequestLog.objects.filter(timestamp__gte=last_24h).count()
    requests_last_7d = RequestLog.objects.filter(timestamp__gte=last_7d).count()

    # Status code breakdown (last 24h)
    status_counts = {}
    recent_logs = RequestLog.objects.filter(timestamp__gte=last_24h)

    for log in recent_logs:
        status = log.response_status or 0
        status_range = f"{status // 100}xx" if status > 0 else "Unknown"
        status_counts[status_range] = status_counts.get(status_range, 0) + 1

    # Top paths (last 24h)
    top_paths = (
        RequestLog.objects.filter(timestamp__gte=last_24h)
        .values('path', 'method')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # Average response time (last 24h)
    avg_response_time = RequestLog.objects.filter(
        timestamp__gte=last_24h, response_time_ms__isnull=False
    ).aggregate(avg_time=Avg('response_time_ms'))

    return {
        'total_requests': total_requests,
        'requests_last_hour': requests_last_hour,
        'requests_last_24h': requests_last_24h,
        'requests_last_7d': requests_last_7d,
        'status_counts': status_counts,
        'top_paths': list(top_paths),
        'avg_response_time': avg_response_time['avg_time'] or 0,
        'updated_at': now.isoformat(),
    }
