from django.db import models



METHOD_CHOICES = [
    ("written", "Written"),
    ("mcq", "MCQ"),
    ("practical", "Practical"),
]
GRADE_TYPE_CHOICES = [
    ("b_side", "B Side"),
    ("y_side", "Y Side"),
]

class AttendanceStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    
    PRESENT = "present", "Present"
    ABSENT = "absent", "Absent"
    LATE = "late", "Late"
    LEAVE = "leave", "Leave"
    