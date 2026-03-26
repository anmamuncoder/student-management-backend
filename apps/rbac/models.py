from django.db import models

# Create your models here.
from kernel.models import BaseModel, AuditModel
from apps.accounts.models import User
from django.utils.text import slugify

class Permission(BaseModel): 
    """Dynamic permission table"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, help_text="Auto-generated from resource and action (e.g., product:view).") #  "product:view"
    resource = models.CharField(max_length=50 , help_text='Specify the resource name this permission applies to (e.g., "product", "order").') # "product"
    action = models.CharField(max_length=50,help_text="Specify the action type (e.g., view, create, update, delete).") # view/update/create/update
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ['resource', 'action']
        ordering = ['resource', 'action']

    def __str__(self):
        return self.slug
    
    def save(self,*args,**kwargs):
        self.slug = f"{slugify(self.resource)}:{slugify(self.action)}".lower()
        super().save(*args,**kwargs)

class Role(BaseModel):
    """ A named group of permissions. 'admin', 'editor', 'viewer' """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    permissions = models.ManyToManyField(Permission,blank=True,related_name='roles')
    description = models.TextField(blank=True)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class UserRole(AuditModel):
    """Maps a user to one or more roles"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
 
    class Meta:
        unique_together = ['user', 'role']

    def __str__(self):
        return f"{self.user} → {self.role}"
