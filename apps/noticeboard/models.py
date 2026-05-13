from django.db import models
from apps.rbac.models import Role
from kernel.models import BaseModel

# Create your models here.
class Event(BaseModel):

    title = models.CharField(max_length=200)

    event_for = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True,blank=True,related_name="events")

    place = models.CharField(max_length=200, null=True, blank=True)

    from_date = models.DateField()
    to_date = models.DateField()

    image = models.ImageField(upload_to="events/images/", null=True, blank=True)
    file = models.FileField(upload_to="events/files/", null=True, blank=True)

    note = models.TextField(null=True, blank=True)

    is_view_on_web = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Notice(BaseModel):

    title = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)

    notice_for = models.ForeignKey(Role, on_delete=models.SET_NULL,null=True,  blank=True, related_name="notices")
    notice = models.TextField()

    is_view_on_web = models.BooleanField(default=True)

    def __str__(self):
        return self.title