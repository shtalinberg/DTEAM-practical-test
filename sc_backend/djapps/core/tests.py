from django.conf import settings
from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_settings_page_shows_debug_value(client):
    """Test that settings page displays DEBUG value from context processor."""
    url = reverse('core:settings_page')
    response = client.get(url)

    assert response.status_code == 200
    assert str(settings.DEBUG) in response.content.decode()
    assert 'settings' in response.context
    assert response.context['settings']['DEBUG'] == settings.DEBUG
