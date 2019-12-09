from datetime import date
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.db import models


GENRE_CHOICES = ["rap", "pop", "rock"]


class User(AbstractUser):
    """Model for a user, who can create playlists and also be associated with songs/albums and thus be an artist."""
    birth_date = models.DateField(null=True, blank=True, validators=[MaxValueValidator(limit_value=date.today)])
    country = CountryField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["country"]),
        ]


class Album(models.Model):
    """Music album model that can be associated with many artists and contain many songs"""
    title = models.CharField(max_length=255)
    # for artists blank=true because request.user is added to the artists in the view after the song is created
    artists = models.ManyToManyField(User, related_name="albums", blank=True)
    # users that have been requested to be added to the artists list and are yet to confirm
    requested_artists = models.ManyToManyField(User, related_name="albums_requested_artist", blank=True)
    release_date = models.DateField(null=True, blank=True, default=date.today, validators=[
                                    MaxValueValidator(limit_value=date.today)])
    cover_image = models.ImageField(upload_to="albums/images", blank=True, null=True)

    def __str__(self):
        return f"Album '{self.title}' by {', '.join([str(artist) for artist in self.artists.all()])}"

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            # indexes on artists are created automatically
        ]


class Song(models.Model):
    """Song model that can be associated with many artists and 0 or 1 albums"""
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to="songs/audio_files", 
                                  validators=[FileExtensionValidator(allowed_extensions=["mp3", "wav", "ogg"])])
    release_date = models.DateField(null=True, blank=True, default=date.today, validators=[
                                    MaxValueValidator(limit_value=date.today)])
    # for artists blank=true because request.user is added to the artists in the view after the song is created
    artists = models.ManyToManyField(User, related_name="songs", blank=True)
    # users that have been requested to be added to the artists list and are yet to confirm
    requested_artists = models.ManyToManyField(User, related_name="songs_requested_artist", blank=True)
    genre = models.CharField(max_length=20, blank=True, null=True, choices=[(g, g) for g in GENRE_CHOICES])
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL, related_name="songs")
    # The song number in the album
    track_number = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    # I put the following validator so that i get a http response instead of integrity error
    duration = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    cover_image = models.ImageField(upload_to="songs/images", blank=True, null=True)

    def __str__(self):
        return f"Song '{self.title}' by {', '.join([str(artist) for artist in self.artists.all()])}"

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["album"]),
            # indexes on artists are created automatically
        ]


class Playlist(models.Model):
    """Music playlist model that is owned by a user and can contain many songs."""
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="playlists", blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Playlist '{self.title}' by user {self.owner}"

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]
