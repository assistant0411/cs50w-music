from django.utils import timezone
from rest_framework import serializers
from .models import User, Song, Playlist, Album
from django_countries.serializers import CountryFieldMixin
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'country', 'password', 'password_confirmation', 'old_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password:
            validate_password(password)
            if password != password_confirmation:
                raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user
        
    def update(self, instance, validated_data):
        password = validated_data.get('password')

        if password:
             if not check_password(validated_data.get('old_password'), instance.password):
                raise serializers.ValidationError("Old password is incorrect.")

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
        exclude = ('artists',)
        extra_kwargs = {
            'audio_file': {'write_only': True},
        }

    def validate_album(self, album):
        # Check if the user is an artist of the album
        if self.context['request'].user not in album.artists.all():
            raise serializers.ValidationError("You must be an artist of the album to add a song to it.")
        
        return album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        exclude = ('artists',)        


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'
        extra_kwargs = {'owner': {'read_only': True}}