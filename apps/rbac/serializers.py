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
    class Meta:
        model = Role
        fields = ['id', 'name', 'slug', 'permissions', 'description', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

 
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