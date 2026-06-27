from django.db import models

# Create your models here.
# Create your models here. 
from kernel.models import BaseModel
from .constants import YesNo, SubjectMethod
from apps.accounts.models import User
from apps.training.models import WeightageDistribution
from django.db.models import Sum


class Course(BaseModel):
    name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=50)
    
    duration = models.CharField(max_length=50, blank=True, null=True)
    vacancy = models.PositiveIntegerField(default=0)

    note = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True,related_name="children")
    
    def __str__(self):
        return self.name
      


class Batch(BaseModel):
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="batches")

    si =  models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="batch_si")
    oic = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="batch_oic")

    batch_start = models.DateField(blank=True, null=True)
    batch_end = models.DateField(blank=True, null=True)

    vacation_option = models.CharField(max_length=3, choices=YesNo.choices, default=YesNo.NO)
    vacation_start = models.DateField(blank=True, null=True)
    vacation_end = models.DateField(blank=True, null=True)

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

        
class Module(BaseModel): 
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True, blank=True, related_name="module_batches")

    name = models.CharField(max_length=150,blank=True,null=True)
    code = models.CharField(max_length=50,blank=True,null=True)
    
    trade = models.CharField(max_length=150, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def total_weightage_with_exams(self):
        """
        Note:
        If a subject has multiple exams, its weightage (wt) will be counted
        once for each exam. For example, if a subject has wt=40 and 2 exams,
        the total contribution will be 80.
        """

        return (
            WeightageDistribution.objects.filter(
                subject__module=self,
                subject__exams__isnull=False
            )
            .aggregate(total=Sum("wt"))
            .get("total")
            or 0
        )

    def __str__(self):
        return f"{self.name} ({self.code})"


class Subject(BaseModel):

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True, blank=True, related_name="batch_subjects")
    module = models.ForeignKey(Module, on_delete=models.CASCADE,null=True, blank=True, related_name="module_subjects")

    name = models.CharField(max_length=150,blank=True,null=True)
    code = models.CharField(max_length=50,blank=True,null=True)
    note = models.TextField(blank=True, null=True)

    # Optional mark distribution
    written_mark = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    practical_mark = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    viva_mark = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    lecture_period = models.CharField(max_length=50, blank=True, null=True)
    practical_period = models.CharField(max_length=50, blank=True, null=True)
    written_period = models.CharField(max_length=50, blank=True, null=True)
    other_period = models.CharField(max_length=50, blank=True, null=True)

    # Academic info
    credit = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    # Method field
    method = models.CharField(max_length=20,choices=SubjectMethod.choices,default=SubjectMethod.LECTURAL)

    instructor =  models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="instructed_subjects")

    def __str__(self):
        if self.name:
            return f"{self.name}"
        return "No Name"


class Syllabus(BaseModel):

    course = models.ForeignKey(Course,on_delete=models.CASCADE, blank=True, null=True,related_name="syllabus_blocks")
    module = models.ForeignKey(Module,on_delete=models.CASCADE, blank=True, null=True, related_name="syllabus_blocks")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, blank=True, null=True, related_name="detail_syllabus")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True, blank=True, related_name="batch_syllabus")

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
        return (
            f"{self.module.name} ({self.module.code})"
            if self.module
            else "No Module Assigned"
        )

        