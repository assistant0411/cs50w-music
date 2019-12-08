"""
Register User, Song, Playlist, Album models in the admin panel.
Use admin.TabularInline to access fields by their related_name.
Use filter_horizontal for enahnced usability.
"""

from django.contrib import admin
from .models import User, Song, Playlist, Album


class ArtistSongInline(admin.TabularInline):
    model = User.songs.through
    extra = 0


class ArtistAlbumInline(admin.TabularInline):
    model = User.albums.through
    extra = 0


class UserPlaylistInline(admin.TabularInline):
    model = Playlist
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [ArtistSongInline, ArtistAlbumInline, UserPlaylistInline]


admin.site.register(User, UserAdmin)


class SongAdmin(admin.ModelAdmin):
    filter_horizontal = ("artists",)


admin.site.register(Song, SongAdmin)


# class AlbumSongInline(admin.TabularInline):
#    model = Song
#    extra = 0


class AlbumAdmin(admin.ModelAdmin):
    # inlines = (AlbumSongInline,)
    filter_horizontal = ("artists", )


admin.site.register(Album, AlbumAdmin)


class PlaylistAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)  # auto_now_add=True in the model and thus can't be editted
    filter_horizontal = ("songs",)


admin.site.register(Playlist, PlaylistAdmin)