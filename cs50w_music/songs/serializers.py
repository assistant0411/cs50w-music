from django.utils import timezone
from rest_framework import serializers
from .models import User, Song, Playlist, Album
from django_countries.serializers import CountryFieldMixin


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

    def validate(self, data):
        release = data.get('release')
        if release and release > timezone.now():
            raise serializers.ValidationError("The release date cannot be in the future.")
        return data


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

    def validate(self, data):
        release = data.get('release')
        if release and release > timezone.now():
            raise serializers.ValidationError("The release date cannot be in the future.")
        return data