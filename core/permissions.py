from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """Allows only owners of an object to watch and edit it."""
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'trip'):
            return obj.trip.user == request.user
        return False