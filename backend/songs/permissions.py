from rest_framework import permissions


class IsArtistOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Deny permission for editing or deleting if the user is not the owner.
        return request.user in obj.artists.all()


class IsPlaylistOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Deny permission if the user is not the owner.
        return obj.owner == request.user


class IsRequestedArtist(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.requested_artists.all()
    

class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow a user to update or delete themselves
        return request.user == obj
    