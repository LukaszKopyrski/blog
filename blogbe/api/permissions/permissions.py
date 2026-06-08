from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request,view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
    

class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return obj.user == request.user or request.user.is_staff
        if request.method == "PATCH":
            return obj.user == request.user
        return False