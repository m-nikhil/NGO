from rest_framework.permissions import BasePermission

class SuperUserPermission(BasePermission):
      def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_superuser

class StaffPermission(BasePermission):
      def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_staff


class NgoPermission(BasePermission):
      def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_ngo

class UserPermission(BasePermission):
      def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return not request.user.is_ngo