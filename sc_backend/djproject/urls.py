from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('cvsai.urls')),
    path('', include('core.urls')),
    path('api/', include('cvsai.api_urls')),
    path('logs/', include('audit.urls')),
    path('admin/', admin.site.urls),
]
