from django.db import models
from apps.course.models import Course, Batch
from apps.student.models import Student

from kernel.models import BaseModel

from django.contrib.auth import get_user_model 
User = get_user_model()
from django.db.models import Q
from .constants import ResultStatus

# Create your models here.
class TrainingProgramme(BaseModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, blank=True, null=True,related_name="training_programme")
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE, blank=True, null=True, related_name="training_programme")
 
    name = models.CharField(max_length=200,null=True,blank=True)
    code = models.CharField(max_length=50,null=True,blank=True)

    description = models.TextField(null=True, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    # -------------------------
    # FILE UPLOAD FIELDS
    # -------------------------
    document = models.FileField(upload_to="syllabus/documents/",null=True, blank=True)
    
    def __str__(self):
        return self.name


class WeightageDistribution(BaseModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, blank=True, null=True,related_name="weightage_distributions")
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE, blank=True, null=True, related_name="weightage_distributions")
    training_programme = models.ForeignKey(TrainingProgramme,on_delete=models.CASCADE, blank=True, null=True, related_name="weightage_distributions")

    topic = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True, blank=True)

    total_marks = models.PositiveIntegerField(default=0)
    practical_marks = models.PositiveIntegerField(default=0)
    theory_marks = models.PositiveIntegerField(default=0)

    percentage = models.FloatField(default=0.0)

    # -------------------------
    # FILE UPLOAD FIELDS
    # -------------------------
    document = models.FileField(upload_to="syllabus/documents/",null=True, blank=True)

    def __str__(self):
        return f"{self.training_programme.name} - {self.topic}"
    

class ObservationSheet(BaseModel):

    course = models.ForeignKey(Course,on_delete=models.CASCADE,blank=True, null=True, related_name="observation_sheets")
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,blank=True, null=True, related_name="observation_sheets")
    student = models.ForeignKey(Student,on_delete=models.CASCADE,blank=True, null=True, related_name="observations")

    index_no = models.PositiveIntegerField(null=True, blank=True)
    observation_date = models.DateField(null=True, blank=True)
    observation_time = models.TimeField(null=True, blank=True)
    observation_note = models.TextField(null=True, blank=True)

    remark = models.TextField(null=True, blank=True)
    observation_mark = models.FloatField(default=0.0)

    point = models.FloatField(default=0.0)

    observation_by= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="created_observations")

    def __str__(self):
        return f"{self.student} - {self.observation_date}"
    

class FinalResult(BaseModel):

    course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True, null=True,  related_name="final_results")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,blank=True, null=True,  related_name="final_results")
    student = models.ForeignKey(Student, on_delete=models.CASCADE,blank=True, null=True,  related_name="final_results")

    training_programme = models.ForeignKey(TrainingProgramme,on_delete=models.SET_NULL,null=True,blank=True,related_name="final_results")

    total_marks = models.FloatField(default=0.0)

    obtained_marks = models.FloatField(default=0.0)

    observation_marks = models.FloatField(default=0.0)

    weightage_marks = models.FloatField(default=0.0)

    final_percentage = models.FloatField(default=0.0)

    grade = models.CharField(max_length=10, null=True, blank=True)

    result_status = models.CharField(max_length=20,choices=ResultStatus.choices,default=ResultStatus.INCOMPLETE)

    remark = models.TextField(null=True, blank=True)
    published_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="published_results")
    published_at = models.DateTimeField(null=True, blank=True)


    # -------------------------
    # FILE UPLOAD FIELDS
    # -------------------------
    document = models.FileField(upload_to="syllabus/documents/",null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.course}"
    