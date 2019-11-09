from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from songs import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'songs', views.SongViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('songs/', include('songs.urls')),
]