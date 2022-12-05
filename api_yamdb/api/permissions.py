from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


def RestrictAnonymousUser(func):
    """
    Перехватывает функции доступа при для анонимного пользователя.
    """

    def has_permission(*args):
        request = args[1]
        # если анонимный пользователь для небезопасных методов
        #  то возвращаем False
        if (request.method not in permissions.SAFE_METHODS
           and isinstance(request.user, AnonymousUser)):
            return False
        res = func(*args)
        return res

    return has_permission


class OnlyAuthorPermission(permissions.BasePermission):
    """
    Глобальная проверка на автора контента.
    """

    @RestrictAnonymousUser
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class OnlyAdministratorPermission(permissions.BasePermission):
    """
    Глобальная проверка на административные права.
    """

    @RestrictAnonymousUser
    def has_object_permission(self, request, view, obj):
        # заменить на реальную проверку!
        return True


class IsAdministratorOrReadinly(permissions.BasePermission):
    """
    Глобальная проверка на административные права.
    """

    @RestrictAnonymousUser
    def has_object_permission(self, request, view, obj):
        # заменить на реальную проверку!
        return True


class NoPermission(permissions.BasePermission):
    """
    Глобальная проверка на административные права.
    """

    @RestrictAnonymousUser
    def has_object_permission(self, request, view, obj):
        # заменить на реальную проверку!
        return False


class AuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Авторизованный пользователь может изменять свой контент.
    Модератор и админ может изменять контент пользователя"""

    @RestrictAnonymousUser
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    @RestrictAnonymousUser
    def has_object_permission(self, request, view, obj):
        stuff = (request.user.is_moderator
                 or request.user.is_admin
                 or request.user.is_superuser)
        return (obj.author == request.user or stuff)


class AdminOrReadOnly(permissions.BasePermission):
    """Права администратора, для остальных только чтение"""

    @RestrictAnonymousUser
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_superuser)


class IsAdmin(permissions.BasePermission):
    """Права только для администратора"""

    @RestrictAnonymousUser
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)
