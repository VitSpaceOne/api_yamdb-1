from rest_framework import permissions


class BaseUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role in self.allowed_roles
            or request.user.is_superuser
        )


class AdminOrReadOnly(BaseUserPermission):

    allowed_roles = ('admin',)


class AdminOrModeratorOrReadOnly(BaseUserPermission):

    allowed_roles = ('admin', 'moderator')


class AdminOrModeratorOrOwnerOrReadOnly(BaseUserPermission):

    allowed_roles = ('admin', 'moderator')

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.role in self.allowed_roles
            or request.user.is_superuser
        )
