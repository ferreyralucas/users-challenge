
from rest_framework import permissions


class UpdateOwnProfileOrStaff(permissions.BasePermission):
    """
    Allows users to edit their own profile or staff users to edit any profile.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff or request.user.is_superuser


class StaffPermission(permissions.BasePermission):
    message = 'You need to be an administrator or a team member to have permission.'

    def has_permission(self, request, view) -> bool:
        """
        Only administrators or team members are allowed to access this endpoint.
        """
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))


class UserRemovalPermission(StaffPermission):

    def has_object_permission(self, request, view, obj) -> bool:
        """
            Clients cannot delete any user.
            Staff users can only delete non-staff users, and only admins can delete any user.
        """
        if request.user.is_staff and not obj.is_staff and not obj.is_superuser:
            return True

        if request.user.is_superuser:
            return True

        return False
