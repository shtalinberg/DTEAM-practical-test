from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('settings/', views.settings_page, name='settings_page'),
]
