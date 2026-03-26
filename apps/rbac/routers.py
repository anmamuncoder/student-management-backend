from rest_framework.routers import DefaultRouter

from .views import (
    PermissionViewSet, 
    RoleViewSet,
    UserRoleViewSet
)

router = DefaultRouter()

router.register(r"permissions",         PermissionViewSet,  basename='rbac-permission')
router.register(r"roles",               RoleViewSet,        basename='rbac-role')
router.register(r'user-roles-assign',   UserRoleViewSet,    basename='rbac-user-role')

