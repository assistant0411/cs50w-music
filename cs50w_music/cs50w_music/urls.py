from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('songs.urls')),
]