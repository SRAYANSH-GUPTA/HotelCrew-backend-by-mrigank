from rest_framework import permissions

class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Manager', 'Admin']
    
class IsNonStaff(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role in ['Manager', 'Admin','Receptionist']
    
class IsNonAdmin(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role in ['Manager', 'Staff','Receptionist']