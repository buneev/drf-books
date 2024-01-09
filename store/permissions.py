from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    has_permission - /api/book/
    has_object_permission - для отдельных записей в базе т.е., /api/book/5/
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            # редактировать книгу могут только тот пользователь,
            # который создал эту книгу, либо админ
            (obj.owner == request.user or request.user.is_staff)
        )

