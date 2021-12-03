from rest_framework.permissions import BasePermission, SAFE_METHODS

METHODS_FOR_MODERATOR = ('PATCH', 'DELETE',)


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in METHODS_FOR_MODERATOR:
            return (
                request.method in SAFE_METHODS
                or request.user == obj.author
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
            )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'
    

class IsAdminOrIsSelf(BasePermission):
   
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or request.user == obj.author
        )

class IsAdminOrReadOnly(BasePermission):
   
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'
 