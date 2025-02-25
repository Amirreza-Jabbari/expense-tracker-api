from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the profile
        return obj.email == request.user.email