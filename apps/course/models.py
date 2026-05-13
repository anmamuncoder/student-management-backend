from django.db import models

# Create your models here.
# Create your models here. 
from kernel.models import BaseModel
from .constants import YesNo
from apps.accounts.models import User

class Course(BaseModel):
    name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=50)
    
    duration = models.CharField(max_length=50, blank=True, null=True)
    vacancy = models.PositiveIntegerField(default=0)

    note = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True,related_name="children")
    
    def __str__(self):
        return self.name
      
class Subject(BaseModel):

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Module(BaseModel): 
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.code})"
 
class Syllabus(BaseModel):

    course = models.ForeignKey(Course,on_delete=models.CASCADE, blank=True, null=True,related_name="syllabus_blocks")
    module = models.ForeignKey(Module,on_delete=models.CASCADE, blank=True, null=True, related_name="syllabus_blocks")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, blank=True, null=True, related_name="detail_syllabus")

    trade = models.CharField(max_length=100, blank=True, null=True) 
 
    lecture = models.PositiveIntegerField(default=0)
    practical = models.PositiveIntegerField(default=0)
    written = models.PositiveIntegerField(default=0)
    others = models.PositiveIntegerField(default=0)

    note = models.TextField(blank=True, null=True)
    # -------------------------
    # FILE UPLOAD FIELDS
    # -------------------------
    document = models.FileField(upload_to="syllabus/documents/",null=True, blank=True)

    def __str__(self):
        return f"{self.module.name} ({self.module.code})"

 
class Batch(BaseModel):
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="batches")

    si =  models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="batch_si")
    oic = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="batch_oic")

    batch_start = models.DateField(blank=True, null=True)
    batch_end = models.DateField(blank=True, null=True)

    vacation_option = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)

    main_mark = models.IntegerField(default=100)
    total_mark = models.IntegerField(default=100)

    comds_obsn_mks = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)
    ci_obsn_mks = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)
    sis_obsn_mks = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)
    oics_obsn_mks = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)

    afvcf_dm = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)
    afvcf_wrls = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)
    ftx_dm = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)
    ftx_gnry = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)
    ftx_wrls = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)

    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

