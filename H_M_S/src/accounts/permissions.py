from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'supervisor'

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'doctor'

class IsNurse(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'nurse'

class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'receptionist'

class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'accountant'

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'patient'

class IsLab(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'lab'

class IsRadiology(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'radiology'

class IsAdminOrSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'supervisor']