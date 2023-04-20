from rest_framework.permissions import BasePermission

class IsOwnerSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_seller and request.user.is_authenticated)

    message = "You must be the owner"

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user.selleruser) or request.user.is_superuser