from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('admin/', admin.site.urls),
    path('restaurant/', include('restaurant.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]
