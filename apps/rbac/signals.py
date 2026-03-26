from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver

from .models import UserRole, Role
from .utils import clear_user_permission_cache, clear_role_permission_cache


@receiver(post_save, sender=UserRole)
@receiver(post_delete, sender=UserRole)
def on_user_role_change(sender, instance, **kwargs):
    """
    Triggered when a user's role is assigned or removed.

    Clears the permission cache for the affected user
    to ensure updated permissions are applied immediately.
    """
    clear_user_permission_cache(instance.user_id)


@receiver(m2m_changed, sender=Role.permissions.through)
def on_role_permission_change(sender, instance, action, **kwargs):
    """
    Triggered when permissions of a role are modified.

    If permissions are added, removed, or cleared from a role,
    all users associated with that role will have their
    permission cache invalidated.
    """
    if action in ("post_add", "post_remove", "post_clear"):
        clear_role_permission_cache(instance)
        