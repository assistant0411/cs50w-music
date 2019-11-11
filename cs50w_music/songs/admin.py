from django.contrib import admin
from .models import UserProfile, Song, Playlist, Album

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Album)