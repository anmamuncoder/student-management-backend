from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView

# Outper Classess
from kernel.responses import BaseResponse
from apps.accounts.models import User

# Inner Classess
from .models import Permission, Role, UserRole
from .serializers import PermissionSerializers, RoleSerializer, UserRoleSerializer
 
 
class SelfPermissionView(APIView):
    """
    Authenticated User can manage permissions.
    Returns permissions grouped by roles for the authenticated user.
    Superusers see all permissions grouped under 'all_permissions'.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {}

        if user.is_superuser:
            # Superuser sees all permissions
            perms = Permission.objects.all()
            perm_slugs = [perm.slug for perm in perms]
            data['admin'] = perm_slugs
        else:
            # Normal user: permissions grouped by their roles
            roles = user.user_roles.select_related('role').prefetch_related('role__permissions')
            for user_role in roles:
                role = user_role.role
                perms = role.permissions.all()
                perm_slugs = [perm.slug for perm in perms]
                data[role.name] = perm_slugs

        return BaseResponse(
            success=True,
            data=data,
            message="Permissions retrieved successfully."
        )


class PermissionViewSet(ReadOnlyModelViewSet):
    """Only admins/superusers can manage permissions. Only GET"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializers
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

class RoleViewSet(ModelViewSet):
    """Only admins/superusers can manage permissions."""
    
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"

class UserRoleViewSet(ModelViewSet):
    """Only admins/superusers can manage permissions."""

    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdminUser]
    