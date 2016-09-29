from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.user == request.user or request.user.is_staff


class IsNotAuthenticated(BasePermission):
    message = "You must be logged out to create a new profile."

    def has_permission(self, request, view):
        return not request.user.is_authenticated() or request.user.is_staff
