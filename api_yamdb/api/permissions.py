from rest_framework.permissions import BasePermission, SAFE_METHODS

METHODS_FOR_MODERATOR = ('PATCH', 'DELETE',)


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
                request.user == obj.author
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
        )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.is_superuser or request.user.role == 'admin')
        )
