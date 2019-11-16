from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils import timezone
from django.core.validators import MaxValueValidator, FileExtensionValidator
from datetime import date


GENRE_CHOICES = ['rap', 'pop', 'rock']


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True, validators=[MaxValueValidator(limit_value=date.today)])
    country = CountryField(null=True, blank=True)

    def __str__(self):
        return self.username


class Album(models.Model):
    title = models.CharField(max_length=255)
    artists = models.ManyToManyField(User, related_name="albums", blank=True)  # blank because request.user is added to the artists in the view
    release_date = models.DateField(null=True, blank=True, default=date.today, validators=[MaxValueValidator(limit_value=date.today)])

    def __str__(self):
        return f"Album '{self.title}' by {', '.join([str(artist) for artist in self.artists.all()])}"


class Song(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='songs/', validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])])
    release_date = models.DateField(null=True, blank=True, default=date.today, validators=[MaxValueValidator(limit_value=date.today)])
    artists = models.ManyToManyField(User, related_name="songs", blank=True)  # blank because request.user is added to the artists in the view
    genre = models.CharField(max_length=20, blank=True, null=True, choices=[(g, g) for g in GENRE_CHOICES])
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL, related_name="songs")
    duration = models.PositiveIntegerField (blank=True, null=True)
    track_number = models.PositiveIntegerField (blank=True, null=True)

    def __str__(self):
        return f"Song '{self.title}' by {', '.join([str(artist) for artist in self.artists.all()])}"


class Playlist(models.Model):
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="playlists", blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Playlist '{self.title}' by user {self.owner}"