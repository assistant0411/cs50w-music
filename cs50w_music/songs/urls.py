from django.urls import path, include
from rest_framework.routers import DefaultRouter
from songs import views


app_name = 'songs'

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'songs', views.SongViewSet)
router.register(r'playlists', views.PlaylistViewSet)
router.register(r'albums', views.AlbumViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:song_id>/play/', views.PlaySongView.as_view(), name='play-song'),
]
