from rest_framework import permissions



class CommitteePermission(permissions.BasePermission):
    """
    Permission for Committee members only.
    """
    message = 'Only committee members are allowed to see feedback list'

    def has_permission(self, request, view):
        if request.user.is_working_group_admin:
            return True
        return False