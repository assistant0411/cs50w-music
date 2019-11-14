from django.urls import path, include
from rest_framework.routers import DefaultRouter
from songs import views
from knox import views as knox_views


app_name = 'songs'

router = DefaultRouter()
router.register(r'songs', views.SongViewSet)
router.register(r'playlists', views.PlaylistViewSet)
router.register(r'albums', views.AlbumViewSet)
router.register(r'users', views.UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('songs/<int:song_id>/play/', views.PlaySongView.as_view(), name='play-song'),
    path('register/', views.RegistrationAPI.as_view(), name='user-register'),
    path('login/', views.LoginAPI.as_view(), name='user-login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox-logout'),
    path('logoutall/',knox_views.LogoutAllView.as_view(), name='knox-logout-all'),
]