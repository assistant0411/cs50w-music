from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils import timezone
from django.core.exceptions import ValidationError


GENRE_CHOICES = ['rap', 'pop', 'rock']


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    country = CountryField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(birth_date__lte=timezone.now()),
                name="check_birth_date_not_in_future"
            )
        ]

    def __str__(self):
        return self.username


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    release = models.DateTimeField(null=True, blank=True, default=timezone.now)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(release__lte=timezone.now()),
                name="check_album_release_not_in_future"
            )
        ]

    def __str__(self):
        return f"Album '{self.title}' by {self.artist}"


def validate_audio_file(value):
    if value.content_type != 'audio/mpeg':
        raise ValidationError("Invalid file type. Only 'audio/mpeg' files are accepted.")


class Song(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='songs/', validators=[validate_audio_file])
    release = models.DateTimeField(null=True, blank=True, default=timezone.now)
    performers = models.ManyToManyField(User, related_name="songs")
    genre = models.CharField(max_length=20, blank=True, null=True, choices=[(g, g) for g in GENRE_CHOICES])
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL, related_name="songs")
    duration = models.PositiveIntegerField (blank=True, null=True)
    track_number = models.PositiveIntegerField (blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(release__lte=timezone.now()),
                name="check_song_release_not_in_future"
            )
        ]

    def __str__(self):
        return f"Song '{self.title}' by {', '.join([str(performer) for performer in self.performers.all()])}"


class Playlist(models.Model):
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, blank=True, related_name="playlists")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Playlist '{self.title}' by user {self.user}"