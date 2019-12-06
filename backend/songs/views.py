from rest_framework import viewsets, permissions, generics
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import User, Song, Playlist, Album
from .serializers import UserSerializer, LoginUserSerializer, SongSerializer, PlaylistSerializer, AlbumSerializer
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import filters
from .permissions import IsArtistOrReadOnly, IsPlaylistOwner, IsUserOrReadOnly, IsRequestedArtist
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    permission_classes = [IsUserOrReadOnly,]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'country']

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RegistrationAPI(generics.GenericAPIView):
    authentication_classes = []
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
    authentication_classes = []
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
    

class SongAlbumMixin:
    def perform_create(self, serializer):
        """Add the current user to the list of artists"""
        entity_instance = serializer.save()
        entity_instance.artists.add(self.request.user)

    @action(detail=True, methods=['delete'])
    def remove_artist(self, request, pk=None):
        """Remove current user from the artists list"""
        entity = self.get_object()
        entity.artists.remove(self.request.user)
        return Response({'detail': 'You have successfully been removed from the artists list.'})

    @action(detail=True, methods=['post'])
    def request_artist(self, request, pk=None):
        """Request to add a user to the artists list"""
        entity = self.get_object()
        artist_id = request.data.get('artist_id', None)

        try:
            artist = User.objects.get(pk=artist_id)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid artist_id.'}, status=status.HTTP_400_BAD_REQUEST)

        entity.requested_artists.add(artist)
        return Response({'detail': 'Artist requested successfully.'})

    @action(detail=True, methods=['post'], permission_classes=[IsRequestedArtist])
    def confirm_artist(self, request, pk=None):
        """Add the current user to the artists list if they are in requested artists."""
        entity = self.get_object()
        entity.artists.add(request.user)
        entity.requested_artists.remove(request.user)
        return Response({'detail': 'You hve successfully been added as an artist.'})
    
    @action(detail=True, methods=['get'])
    def get_image(self, request, pk=None):
        entity = self.get_object()

        if entity.cover_image:
            return FileResponse(entity.cover_image, 'image/*')
        else:
            return Response({'detail': 'Image not found'}, status=404)

class SongViewSet(SongAlbumMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Songs to be viewed or edited.
    """
    queryset = Song.objects.all().order_by('-release_date')
    serializer_class = SongSerializer
    permission_classes = [IsArtistOrReadOnly,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'artists']

    @action(detail=True, methods=['get'])
    def play(self, request, pk=None):
        song = self.get_object()
        return FileResponse(song.audio_file, content_type='audio/mpeg')


class AlbumViewSet(SongAlbumMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Albums to be viewed or edited.
    """
    queryset = Album.objects.all().order_by('-release_date')
    serializer_class = AlbumSerializer
    permission_classes = [IsArtistOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'artists']


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Playlists to be viewed or edited.
    """
    queryset = Playlist.objects.all().order_by('-created_at')
    serializer_class = PlaylistSerializer
    permission_classes = [IsPlaylistOwner, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title',]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def manage_songs(self, request, pk=None):
        """Add or remove a song to/from a playlist."""

        playlist = self.get_object()
        song_id = request.data.get('song_id', None)

        try:    
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response({'detail': 'Invalid song_id.'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            playlist.songs.add(song)
            message = 'Song added successfully.'
        elif request.method == 'DELETE':
            playlist.songs.remove(song)
            message = 'Song removed successfully.'

        return Response({'detail': message})
