from rest_framework import viewsets, permissions, generics
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import User, Song, Playlist, Album
from .serializers import UserSerializer, LoginUserSerializer, SongSerializer, PlaylistSerializer, AlbumSerializer
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import filters
from .permissions import IsArtistOrReadOnly, IsPlaylistOwnerOrReadOnly, IsUserOrReadOnly
from django.shortcuts import render
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import action


def index(request):
    return render(request, "songs/index.html")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    permission_classes = [permissions.IsAuthenticated, IsUserOrReadOnly]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_201_CREATED)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Songs to be viewed or edited.
    """
    queryset = Song.objects.all().order_by('-release_date')
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated, IsArtistOrReadOnly]

    def perform_create(self, serializer):
        # Save the album and then add the current user to the artists
        song = serializer.save()
        song.artists.add(self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def manage_artists(self, request, pk=None):
        song = self.get_object()
        artist_ids = []

        artist_ids = request.data.getlist('artist_ids', [])
        artists = User.objects.filter(id__in=artist_ids)

        if request.method == 'POST':
            song.artists.add(*artists)
            message = 'Artists added successfully.'

        elif request.method == 'DELETE':
            song.artists.remove(*artists)
            message = 'Artists removed successfully.'

        return Response({'detail': message})
    
    @action(detail=True, methods=['get'])
    def play(self, request, pk=None):
        song = self.get_object()
        return FileResponse(song.audio_file, content_type='audio/mpeg')

    

class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Playlists to be viewed or edited.
    """
    queryset = Playlist.objects.all().order_by('-created_at')
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsPlaylistOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def manage_songs(self, request, pk=None):
        playlist = self.get_object()

        song_ids = request.data.getlist('song_ids', [])
        songs = Song.objects.filter(id__in=song_ids)

        if request.method == 'POST':
            playlist.songs.add(*songs)
            message = 'Songs added successfully.'

        elif request.method == 'DELETE':
            playlist.songs.remove(*songs)
            message = 'Songs removed successfully.'

        return Response({'detail': message})


class AlbumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Albums to be viewed or edited.
    """
    queryset = Album.objects.all().order_by('-release_date')
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated, IsArtistOrReadOnly]

    def perform_create(self, serializer):
        # Save the album and then add the current user to the artists
        album = serializer.save()
        album.artists.add(self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def manage_artists(self, request, pk=None):
        album = self.get_object()
        artist_ids = []

        artist_ids = request.data.getlist('artist_ids', [])
        artists = User.objects.filter(id__in=artist_ids)

        if request.method == 'POST':
            album.artists.add(*artists)
            message = 'Artists added successfully.'

        elif request.method == 'DELETE':
            album.artists.remove(*artists)
            message = 'Artists removed successfully.'

        return Response({'detail': message})