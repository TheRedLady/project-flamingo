from rest_framework.permissions import BasePermission


class PostsPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return request.user.is_authenticated()
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_authenticated() and obj.posted_by == request.user
        else:
            return False
