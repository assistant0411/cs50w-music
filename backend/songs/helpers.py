from notifications.signals import notify
from rest_framework import status
from rest_framework.response import Response


def add_artist_to_requested(entity, artist, requester):
    if artist not in entity.artists.all() and artist not in entity.requested_artists.all():
        entity.requested_artists.add(artist)
        verb = f"{requester} requested to add you as an artist of {entity}"
        notify.send(requester, recipient=artist, verb=verb, target=entity, public=False)
        return Response({"detail": "Artist requested."})
    else:
        return Response({"detail": "The user is already an artist or requested."}, status=status.HTTP_409_CONFLICT)


def remove_artist_from_requested(entity, artist, requester):
    if artist in entity.requested_artists.all():
        entity.requested_artists.remove(artist)
        verb = f"{requester} canceled the request to add you as an artist of {entity}"
        notify.send(requester, recipient=artist, verb=verb, target=entity, public=False)
        return Response({"detail": "Request cancelled."})
    else:
        return Response({"detail": "The user is not a requested artist."}, status=status.HTTP_409_CONFLICT)

    
def confirm_user_as_artist(entity, user):
    entity.artists.add(user)
    entity.requested_artists.remove(user)
    verb = f"{user.username} confirmed the request to be added as an artist of {entity}"

    for artist in entity.artists.exclude(pk=user.id):
        notify.send(user, recipient=artist, verb=verb, target=entity, public=False)

    return Response({"detail": "You have successfully been added as an artist."})


def remove_user_as_artist(entity, user):
    entity.artists.remove(user)
    verb = f"{user.username} removed themselves as an artist of {entity}"
    
    for artist in entity.artists.all():
        notify.send(user, recipient=artist, verb=verb, target=entity, public=False)

    return Response({"detail": "You have successfully been removed from the artists list."})

        
def add_song_to_playlist(playlist, song):
    if song not in playlist.songs.all():
        playlist.songs.add(song)
        return Response({"detail": "Song added successfully."})
    else:
        return Response({"detail": "The song is already in the playlist"}, status=status.HTTP_409_CONFLICT)


def remove_song_from_playlist(playlist, song):
    if song in playlist.songs.all():
        playlist.songs.remove(song)
        return Response({"detail": "Song removed successfully."})
    else:
        return Response({"detail": "The song is not in the playlist"}, status=status.HTTP_409_CONFLICT)
