from django.http import JsonResponse
from rest_framework import status

from kernel.responses import BaseResponse
from .utils import get_user_permissions
from functools import wraps

# def require_permission(perm_slug: str):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(view_or_self, request, *args, **kwargs):
#             return func(view_or_self, request, *args, **kwargs)
#         return wrapper
#     return decorator

def require_permission(perm_slug: str):
    """
    Ensures that the authenticated user has a specific permission.

    Use this decorator for custom actions where middleware-based
    permission handling is not sufficient.

    Example:
        from rbac.decorators import require_permission

        class ReportViewSet(viewsets.ModelViewSet):

            @action(detail=False, methods=['get'])
            @require_permission('report:export')
            def export(self, request):
                ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(view_or_self, request, *args, **kwargs):
            user = request.user

            # Check authentication
            if not user or not user.is_authenticated:
                return BaseResponse(
                    message="Authentication required",
                    success=False,
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Allow superuser bypass
            if user.is_superuser:
                return func(view_or_self, request, *args, **kwargs)

            # Fetch user permissions
            user_perms = get_user_permissions(user)

            # Check required permission
            if perm_slug not in user_perms:
                return BaseResponse(
                    data={"required_permission": perm_slug},
                    message="You do not have permission to perform this action.",
                    success=False,
                    status=status.HTTP_403_FORBIDDEN
                )

            return func(view_or_self, request, *args, **kwargs)

        return wrapper
    return decorator


def require_any_permission(*perm_slugs: str):
    """
    Ensures that the authenticated user has at least one
    of the given permissions.

    Example:
        @require_any_permission('report:view', 'report:create')
        def export(self, request):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(view_or_self, request, *args, **kwargs):
            user = request.user

            # Check authentication
            if not user or not user.is_authenticated:
                return BaseResponse(
                    message="Authentication required",
                    success=False,
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Allow superuser bypass
            if user.is_superuser:
                return func(view_or_self, request, *args, **kwargs)

            # Fetch user permissions
            user_perms = get_user_permissions(user)

            # Check if any required permission exists
            if not user_perms.intersection(perm_slugs):
                return BaseResponse(
                    data={"required_any": list(perm_slugs)},
                    message="You do not have permission to perform this action.",
                    success=False,
                    status=status.HTTP_403_FORBIDDEN
                )

            return func(view_or_self, request, *args, **kwargs)

        return wrapper
    return decorator
