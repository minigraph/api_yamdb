from rest_framework import permissions


class AuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Авторизованный пользователь может изменять свой контент.
    Модератор и админ может изменять контент пользователя"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        stuff = (request.user.is_authenticated
                 and (request.user.is_moderator
                      or request.user.is_admin
                      or request.user.is_superuser))
        return (request.method in permissions.SAFE_METHODS
                or (obj.author == request.user or stuff))


class AdminOrReadOnly(permissions.BasePermission):
    """Права администратора, для остальных только чтение"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin
                         or request.user.is_superuser)))

    def has_object_permission(self, request, view, obj):
        stuff = (request.user.is_authenticated
                 and (request.user.is_moderator
                      or request.user.is_admin
                      or request.user.is_superuser))
        return (request.method in permissions.SAFE_METHODS
                or stuff)


class IsAdmin(permissions.BasePermission):
    """Права только для администратора"""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)
