from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsExaminerOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # Everyone can read
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Read allowed for everyone
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        # superuser bypass
        if user.is_superuser:
            return True

        # admin role bypass
        if user.user_roles.filter(role__slug="admin").exists():
            return True

        # only examiner can modify
        return obj.exam.examiner == user
    