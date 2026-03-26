from django.contrib import admin

# Register your models here. 
from .models import Permission, Role, UserRole


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display  = ['slug', 'name', 'resource', 'action']
    list_filter   = ['resource', 'action']
    search_fields = ['slug', 'name', 'resource']
    ordering      = ['resource', 'action'] 
    readonly_fields = ['created_at', 'updated_at']

    prepopulated_fields = {
            "slug": ("resource", "action"),
        }

class PermissionInline(admin.TabularInline):
    model = Role.permissions.through
    extra = 0
    verbose_name = 'Permission'
    verbose_name_plural = 'Permissions'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display   = ['name', 'slug', 'permission_count', 'user_count', 'created_at']
    search_fields  = ['name', 'slug']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    filter_horizontal = ['permissions']

    def permission_count(self, obj):
        return obj.permissions.count()
    permission_count.short_description = 'Permissions'

    def user_count(self, obj):
        return obj.user_roles.count()
    user_count.short_description = 'Users'


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display  = ['user', 'role', 'created_by', 'created_at']
    list_filter   = ['role']
    search_fields = ['user__email', 'role__name']
    raw_id_fields = ['user', 'created_by']
    readonly_fields = ['created_at']
