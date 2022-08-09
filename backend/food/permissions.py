from rest_framework import permissions


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.method in ("PATCH", "DELETE") and (
            request.user
            and (
                (request.user.role in ("admin",) or request.user.is_staff)
                or obj.author == request.user
            )
        )