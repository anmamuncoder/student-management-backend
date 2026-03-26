from django.core.cache import cache

from .models import Permission
from .config import URL_PERMISSION_MAP, HTTP_METHOD_ACTION_MAP, EXEMPT_PATHS

import re 

# ------------------------------
# Get Resource from Path
# ------------------------------
def _get_resource_from_path(path: str) -> str:
    """
    URL API Path to resource name
    '/api/v1/products/123/' -> 'product'
    """ 
    for pattern, resource in URL_PERMISSION_MAP:
        if re.match(pattern, path):
            return resource
    return None

def _is_exempt(path: str) -> bool:
    """ Check the path is exempt from permisison"""
    return any(re.match(pattern, path) for pattern in EXEMPT_PATHS)


# ------------------------------
# Get User Permissions
# ------------------------------
def get_user_permissions(user) -> set:
    """
    Return all permission slug of any User
    take catch for 5 minutes

    Returns:
        set of permission slugs, e.g. {"product:view", "order:create"}
    """

    cache_key = f"rbac:user_perms:{user.id}"
    perms = cache.get(cache_key)
    # perms = None

    if perms is None:
        perms = set(Permission.objects.filter(roles__user_roles__user=user).values_list('slug',flat=True))
        cache.set(cache_key,perms,timeout=300) # 5 min
    return perms

# ------------------------------
# Clear-Cache User Permissions
# ------------------------------
def clear_user_permission_cache(user_id: int):
    cache.delete(f"rbac:user_perms:{user_id}")


def clear_role_permission_cache(role):
    for user_role in role.user_roles.select_related('user').all():
        clear_user_permission_cache(user_role.user_id)

# ------------------------------
# Permission Check
# ------------------------------
def user_has_permission(user, perm_slug: str) -> bool:
    """Shortcut: single permission check."""
    if user.is_superuser:
        return True
    return perm_slug in get_user_permissions(user)

def user_has_any_permission(user, perm_slugs: list) -> bool:
    if user.is_superuser:
        return True
    user_perms = get_user_permissions(user)
    return bool(user_perms.intersection(perm_slugs))

def user_has_all_permissions(user, perm_slugs: list) -> bool:
    if user.is_superuser:
        return True
    user_perms = get_user_permissions(user)
    return set(perm_slugs).issubset(user_perms)
