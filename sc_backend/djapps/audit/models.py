from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RequestLog(models.Model):
    """Model for logging HTTP requests."""

    timestamp = models.DateTimeField(
        verbose_name=_("Timestamp"),
        auto_now_add=True,
        help_text=_("When the request was made"),
    )
    method = models.CharField(
        verbose_name=_("HTTP Method"),
        max_length=10,
        help_text=_("HTTP method (GET, POST, PUT, etc.)"),
    )
    path = models.CharField(
        verbose_name=_("Path"), max_length=1024, help_text=_("Request path")
    )
    query_string = models.TextField(
        verbose_name=_("Query String"), blank=True, help_text=_("URL query parameters")
    )
    remote_ip = models.GenericIPAddressField(
        verbose_name=_("Remote IP"),
        null=True,
        blank=True,
        help_text=_("Client IP address"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Authenticated user (if any)"),
    )
    user_agent = models.TextField(
        verbose_name=_("User Agent"),
        blank=True,
        help_text=_("Browser/client information"),
    )
    response_status = models.PositiveIntegerField(
        verbose_name=_("Response Status"),
        null=True,
        blank=True,
        help_text=_("HTTP response status code"),
    )
    response_time_ms = models.PositiveIntegerField(
        verbose_name=_("Response Time (ms)"),
        null=True,
        blank=True,
        help_text=_("Request processing time in milliseconds"),
    )

    class Meta:
        verbose_name = _("Request Log")
        verbose_name_plural = _("Request Logs")
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['method']),
            models.Index(fields=['path']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        user_info = f" ({self.user.username})" if self.user else ""
        return f"{self.method} {self.path}{user_info} - {self.timestamp}"

    @property
    def formatted_timestamp(self):
        """Return formatted timestamp for display."""
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def is_api_request(self):
        """Check if this is an API request."""
        return self.path.startswith('/api/')

    @property
    def status_class(self):
        """Return CSS class based on response status."""
        if not self.response_status:
            return 'secondary'

        if 200 <= self.response_status < 300:
            return 'success'
        if 300 <= self.response_status < 400:
            return 'info'
        if 400 <= self.response_status < 500:
            return 'warning'
        if self.response_status >= 500:
            return 'danger'
        return 'secondary'
