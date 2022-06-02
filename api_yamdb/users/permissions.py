from rest_framework import permissions


class Superuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class Admin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'


class Modertor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'moderator'


class Owner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS