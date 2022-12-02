from rest_framework import permissions


class OnlyAuthorPermission(permissions.BasePermission):
    """
    Глобальная проверка на автора контента.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class OnlyAdministratorPermission(permissions.BasePermission):
    """
    Глобальная проверка на административные права.
    """

    def has_object_permission(self, request, view, obj):
        # заменить на реальную проверку!
        return True


class IsAdministratorOrReadinly(permissions.BasePermission):
    """
    Глобальная проверка на административные права.
    """

    def has_object_permission(self, request, view, obj):
        # заменить на реальную проверку!
        return True


class NoPermission(permissions.BasePermission):
    """
    Глобальная проверка на административные права.
    """

    def has_object_permission(self, request, view, obj):
        # заменить на реальную проверку!
        return False
