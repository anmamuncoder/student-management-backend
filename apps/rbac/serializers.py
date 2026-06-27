from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.rbac.models import Permission, Role, UserRole

User = get_user_model()

class PermissionSerializers(ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id','slug','name','resource','action','description','created_at','updated_at')
        read_only_fields = ['slug', 'created_at', 'updated_at'] 


class RoleSerializer(serializers.ModelSerializer):

    # Always use a slug list for permissions
    permissions = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Permission.objects.all()
    )

    PROTECTED_ROLES = {
        "admin",
        "instructors",
        "oic",
        "si",
        "staff",
        "librarian",
    }

    class Meta:
        model = Role
        fields = ['id', 'name', 'slug','group', 'permissions', 'description', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def validate(self, attrs):
        instance = getattr(self, "instance", None)

        if instance and instance.slug in self.PROTECTED_ROLES:
            if "name" in attrs and attrs["name"] != instance.name:
                raise serializers.ValidationError({
                    "name": "This role name cannot be changed."
                })

        return attrs

class UserRoleSerializer(ModelSerializer):
    # Accept role by slug
    
    role = serializers.SlugRelatedField(
        queryset=Role.objects.all(),
        slug_field='slug'
    )
    
    # Accept user by ID
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='email'

    )
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role']