from rest_framework import permissions


class AuthorAndStaffOrReadOnly(permissions.BasePermission):
    """Авторизованный пользователь может изменять свой контент.
    Модератор и админ может изменять контент пользователя"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        stuff = (request.user.role.moderator
                 or request.user.role.admin
                 or request.user.is_superuser)
        return (obj.author == request.user or stuff)
