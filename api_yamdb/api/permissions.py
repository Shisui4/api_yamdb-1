from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmimOrIsSelf(BasePermission):
   
    def has_permission(self, request, view):
        return  request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or request.user == obj.author
        )