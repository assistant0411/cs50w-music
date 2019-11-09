from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from songs.models import Song
from songs.serializers import UserSerializer, GroupSerializer, SongSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Song.objects.all().order_by('-release')
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlaySongView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        return FileResponse(song.audio_file, content_type='audio/mpeg')