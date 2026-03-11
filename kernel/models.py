from django.db import models
# Importing from Midilleware 
from kernel.middleware.current_user import get_current_user
from django.conf import settings
import uuid


# BaseModel to track created_at and updated_at fields,
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False,db_index=True)
    updated_at = models.DateTimeField(auto_now=True,editable=False)

    class Meta:
        abstract = True

# AuditModel to track created_by and updated_by fields,  
class AuditModel(BaseModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,editable=False, related_name="%(class)s_created",)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,editable=False,related_name="%(class)s_updated",)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()

        if user and user.is_authenticated:

            if self._state.adding and not self.created_by:
                self.created_by = user

            self.updated_by = user

        super().save(*args, **kwargs)