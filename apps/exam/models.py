from django.db import models

from apps.course.models import Course,Batch,Module,Subject
from apps.student.models import Student
from .constants import METHOD_CHOICES,  GRADE_TYPE_CHOICES
from kernel.models import BaseModel

# -------------------------
# Grading System
# -------------------------
class ExamGrade(BaseModel):
    b_side_grade = models.CharField(max_length=10)
    y_side_grade = models.CharField(max_length=10)

    grade_point = models.FloatField()

    mark_from = models.PositiveIntegerField()
    mark_to = models.PositiveIntegerField()

    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.b_side_grade} ({self.mark_from}-{self.mark_to})"
 
# -------------------------
# Exam Schedule
# -------------------------
class ExamSchedule(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)


    method = models.CharField(max_length=20, choices=METHOD_CHOICES, blank=True, null=True)

    exam_date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    room_no = models.CharField(max_length=50)


    grade_type = models.CharField(max_length=20, choices=GRADE_TYPE_CHOICES)

    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject} - {self.exam_date}"
 
# -------------------------
# Exam (optional wrapper)
# -------------------------
class Exam(BaseModel):
    name = models.CharField(max_length=255)
    schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name="exams")

    def __str__(self):
        return self.name


# -------------------------
# Attendance
# -------------------------
class ExamAttendance(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    is_present = models.BooleanField(default=False)

 
    def __str__(self):
        return f"{self.student.name} - {self.exam.name}"
    

