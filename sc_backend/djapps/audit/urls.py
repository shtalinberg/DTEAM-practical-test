from django.urls import path

from . import views

app_name = 'audit'

urlpatterns = [
    path('', views.log_requests, name='log_requests'),  # Alternative URL
    path('recent/', views.recent_requests, name='recent_requests'),
    path('stats/', views.request_stats_api, name='stats_api'),
]
