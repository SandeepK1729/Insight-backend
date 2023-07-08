from rest_framework.permissions     import BasePermission

class IsModelEdit(BasePermission):
    """Permssion to requested is user manager"""
    
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_staff
        )