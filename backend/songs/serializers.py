from django.utils import timezone
from rest_framework import serializers
from .models import User, Song, Playlist, Album
from django_countries.serializers import CountryFieldMixin
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password as django_contrib_validate_password
from django.contrib.auth.hashers import check_password


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'country', 'password', 'password_confirmation', 'old_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    # so that the raised error is not non_field_errors
    def validate_password(self, password):
        django_contrib_validate_password(password)
        return password

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password and password != password_confirmation:
            raise serializers.ValidationError(
                {"password_confirmation": "Password confirmation does not match password."}
            )

        return data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        """Exclude email for other users"""

        if self.context['request'].user != instance:
            del representation['email']

        return representation

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user
        
    def update(self, instance, validated_data):
        password = validated_data.get('password')
        old_password = validated_data.get('old_password')

        if password and not check_password(old_password, instance.password):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})

        return super().update(instance, validated_data)
    

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        exclude = ('requested_artists',)
        extra_kwargs = {
            'audio_file': {'write_only': True},
            'artists': {'read_only': True},
            'song_cover_image': {'write_only': True},
        }

    def validate_album(self, album):
        # Check if the user is an artist of the album
        if self.context['request'].user not in album.artists.all():
            raise serializers.ValidationError({"album": "You must be an artist of the album to add a song to it."})
        
        return album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        exclude = ('requested_artists',)
        extra_kwargs = {
            'artists': {'read_only': True},
            'album_cover_image': {'write_only': True},
        }    


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'
        extra_kwargs = {'owner': {'read_only': True}}