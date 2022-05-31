from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )


class AdminOrModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role in ('admin', 'moderator')
            or request.user.is_superuser
        )


class AdminOrModeratorOrOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role in ('admin', 'moderator')
            or request.user.is_superuser
            or request.user == obj.author
        )
