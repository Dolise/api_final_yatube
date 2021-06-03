from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Is used to set permission to change objects only for owner."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
