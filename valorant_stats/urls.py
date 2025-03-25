from django.contrib import admin
from django.urls import path, include
from stats.api.routes import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', include('stats.urls')),
]
