from django.utils import timezone
from rest_framework import serializers
from .models import User, Song, Playlist, Album
from django_countries.serializers import CountryFieldMixin
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password, ValidationError as PasswordValidationError


class CreateUserSerializer(serializers.ModelSerializer):

    password_confirmation = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation', 'birth_date', 'country')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        validate_password(data['password'])

        if data.get('password') != data.get('password_confirmation'):
            raise serializers.ValidationError("Passwords do not match")
        
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")
    

class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'country', 'birth_date')


class SongAndAlbumMixinWithValidation(metaclass=serializers.SerializerMetaclass):
    artists = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)

    def validate(self, data):
        release = data.get('release')
        if release and release > timezone.now():
            raise serializers.ValidationError("The release date cannot be in the future.")
        return data

    def create(self, validated_data):
        curr_user = self.context['request'].user
        additional_artists = validated_data.pop('artists', [])

        instance = self.Meta.model.objects.create(**validated_data)

        instance.artists.add(curr_user)

        for artist in additional_artists:
            instance.artists.add(artist)

        return instance


class SongSerializer(SongAndAlbumMixinWithValidation, serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class AlbumSerializer(SongAndAlbumMixinWithValidation, serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'
        extra_kwargs = {'owner': {'read_only': True}}