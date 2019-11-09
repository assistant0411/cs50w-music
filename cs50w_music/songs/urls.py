from django.urls import path
from .views import PlaySongView


app_name = 'songs'

urlpatterns = [
    path('<int:song_id>/play/', PlaySongView.as_view(), name='play-song'),
]
