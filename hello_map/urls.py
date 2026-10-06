from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from mapping.views import map_view

urlpatterns = [
    # Week 4: Leaflet frontend for the cities API
    path('', TemplateView.as_view(template_name='map.html'), name='map'),
    path('map/', TemplateView.as_view(template_name='map.html'), name='cities-map'),

    # Week 1 hello map kept available
    path('hello/', map_view, name='hello-map'),

    path('admin/', admin.site.urls),
    path('spatial/', include('spatial_analysis.urls')),

    # Week 3: API endpoints
    path('api/cities/', include('cities_api.urls')),

    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
