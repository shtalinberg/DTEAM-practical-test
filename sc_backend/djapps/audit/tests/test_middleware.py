from django.contrib.auth.models import User
from django.test import Client, RequestFactory
from django.urls import reverse

import pytest

from audit.middleware import RequestLoggingMiddleware
from audit.models import RequestLog


@pytest.mark.django_db
class TestRequestLoggingMiddleware:
    """Test cases for RequestLoggingMiddleware."""

    @pytest.fixture
    def middleware(self):
        """Create middleware instance."""
        return RequestLoggingMiddleware(get_response=lambda request: None)

    @pytest.fixture
    def factory(self):
        """Request factory for creating mock requests."""
        return RequestFactory()

    @pytest.fixture
    def user(self):
        """Create a test user."""
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_get_client_ip_from_remote_addr(self, middleware, factory):
        """Test getting client IP from REMOTE_ADDR."""
        request = factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.100'

        ip = middleware._get_client_ip(request)
        assert ip == '192.168.1.100'

    def test_get_client_ip_from_forwarded_headers(self, middleware, factory):
        """Test getting client IP from forwarded headers."""
        request = factory.get('/')
        ip_xforwarded_for_list = '203.0.113.195, 70.41.3.18, 150.172.238.178'
        request.META['HTTP_X_FORWARDED_FOR'] = ip_xforwarded_for_list

        ip = middleware._get_client_ip(request)
        assert ip == '203.0.113.195'  # Should take first IP


@pytest.mark.django_db
class TestRequestLoggingIntegration:
    """Integration tests for request logging."""

    @pytest.fixture
    def client(self):
        """Django test client."""
        return Client()

    @pytest.fixture
    def user(self):
        """Create a test user."""
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_get_request_is_logged(self, client):
        """Test that a request is properly logged."""
        initial_count = RequestLog.objects.count()

        # Make a request
        response = client.get('/')

        # Check that log was created
        assert RequestLog.objects.count() == initial_count + 1

        # Check log details
        log = RequestLog.objects.latest('timestamp')
        assert log.method == 'GET'
        assert log.path == '/'
        assert log.response_status == response.status_code
        assert log.user is None  # Anonymous user

    def test_authenticated_user_request_is_logged(self, client, user):
        """Test that authenticated user requests are logged with user info."""
        client.force_login(user)
        initial_count = RequestLog.objects.count()

        # Make a request
        response = client.get('/')

        # Check that log was created with user
        assert RequestLog.objects.count() == initial_count + 1

        log = RequestLog.objects.latest('timestamp')
        assert log.method == 'GET'
        assert log.path == '/'
        assert log.user == user
        assert log.response_status == response.status_code

    def test_request_is_logged(self, client):
        """Test that POST requests are logged."""
        initial_count = RequestLog.objects.count()

        # Make a POST request (will likely return 404 or 405, but should be logged)
        response = client.post('/nonexistent/', {'data': 'test'})

        # Check that log was created
        assert RequestLog.objects.count() == initial_count + 1

        log = RequestLog.objects.latest('timestamp')
        assert log.method == 'POST'
        assert log.path == '/nonexistent/'
        assert log.response_status == response.status_code

        # Make a request with query parameters
        response = client.get('/?page=2&filter=test')

        # Check that log was created with query string
        assert RequestLog.objects.count() == initial_count + 2

        log = RequestLog.objects.latest('timestamp')
        assert log.method == 'GET'
        assert log.path == '/'
        assert 'page=2&filter=test' in log.query_string

    def test_static_files_not_logged(self, client):
        """Test that static file requests are not logged."""
        initial_count = RequestLog.objects.count()

        # Make requests to static paths
        static_paths = [
            '/static/css/style.css',
            '/media/uploads/test.jpg',
            '/favicon.ico',
        ]

        for path in static_paths:
            client.get(path)

        # Check that no logs were created
        assert RequestLog.objects.count() == initial_count


@pytest.mark.django_db
class TestRequestLogViews:
    """Test cases for request log views."""

    @pytest.fixture
    def client(self):
        """Django test client."""
        return Client()

    @pytest.fixture
    def sample_logs(self, user):
        """Create sample request logs."""
        logs = []
        for i in range(15):
            log = RequestLog.objects.create(
                method='GET' if i % 2 == 0 else 'POST',
                path=f'/test/path/{i}/',
                query_string='param=value' if i % 3 == 0 else '',
                remote_ip='192.168.1.100',
                user=user if i % 4 == 0 else None,
                user_agent='Mozilla/5.0 Test Browser',
                response_status=200 if i % 5 != 0 else 404,
                response_time_ms=100 + (i * 10)
            )
            logs.append(log)
        return logs

    @pytest.fixture
    def user(self):
        """Create a test user."""
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_recent_requests_view_simple(self, client, sample_logs):
        """Test the simple recent requests view (task requirement)."""
        url = reverse('audit:recent_requests')
        response = client.get(url)

        assert response.status_code == 200
        assert 'recent_logs' in response.context

        # Should show exactly 10 most recent logs
        assert len(response.context['recent_logs']) == 10

        # Should be ordered by timestamp descending (most recent first)
        logs = response.context['recent_logs']
        for i in range(len(logs) - 1):
            assert logs[i].timestamp >= logs[i + 1].timestamp

    def test_log_requests_view_advanced(self, client, sample_logs):
        """Test the advanced log requests view with pagination."""
        url = reverse('audit:log_requests')
        response = client.get(url)

        assert response.status_code == 200
        assert 'page_obj' in response.context
        assert 'stats' in response.context

        # Check that logs are displayed (default pagination is 20)
        assert len(response.context['page_obj']) == 15
