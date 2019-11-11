from rest_framework import viewsets, permissions
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from songs.models import UserProfile, Song, Playlist, Album
from songs.serializers import UserProfileSerializer, SongSerializer, PlaylistSerializer, AlbumSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows UserProfiles to be viewed or edited.
    """
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Songs to be viewed or edited.
    """
    queryset = Song.objects.all().order_by('-release')
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlaySongView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        return FileResponse(song.audio_file, content_type='audio/mpeg')
    

class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Playlists to be viewed or edited.
    """
    queryset = Playlist.objects.all().order_by('-created_at')
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlbumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Albums to be viewed or edited.
    """
    queryset = Album.objects.all().order_by('-release')
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]