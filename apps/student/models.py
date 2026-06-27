from django.db import models

from django.contrib.auth import get_user_model
from kernel.models import BaseModel
from apps.course.models import Course, Batch
from .constants import QualificationType
User = get_user_model()
from django.db.models import Q


# ----------------------------
# STUDENT CORE MODEL
# ----------------------------
class Student(BaseModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # -------------------------
    # Academic Info
    # -------------------------
    student_type = models.ForeignKey("StudentType", on_delete=models.SET_NULL, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)

    second_language = models.CharField(max_length=50, blank=True, null=True)

    date_of_commission = models.DateField(null=True, blank=True)
    date_of_joining_accs = models.DateField(null=True, blank=True)

    # -------------------------
    # Family Information
    # -------------------------
    father_full_name = models.CharField(max_length=100, blank=True, null=True)
    father_phone = models.CharField(max_length=20, blank=True, null=True)
    father_address = models.TextField(blank=True, null=True)
    father_profession = models.CharField(max_length=100, blank=True, null=True)
    father_designation = models.CharField(max_length=100, null=True, blank=True)
    father_photo = models.ImageField(upload_to="father/", null=True, blank=True)

    mother_full_name = models.CharField(max_length=100, blank=True, null=True)
    mother_phone = models.CharField(max_length=20, blank=True, null=True)
    mother_address = models.TextField(blank=True, null=True)
    mother_profession = models.CharField(max_length=100, blank=True, null=True)
    mother_designation = models.CharField(max_length=100, null=True, blank=True)
    mother_photo = models.ImageField(upload_to="mother/", null=True, blank=True)
    # -------------------------
    # Passport
    # -------------------------
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    passport_issue_date = models.DateField(null=True, blank=True)
    passport_place = models.CharField(max_length=100, blank=True, null=True)
    passport_expiry_date = models.DateField(null=True, blank=True)

    # -------------------------
    # Health / Other
    # -------------------------
    health_condition = models.TextField(blank=True, null=True)
    other_info = models.TextField(blank=True, null=True)

    discount = models.IntegerField(default=0, null=True, blank=True)
    previous_school = models.CharField(max_length=150, null=True, blank=True)
    previous_class = models.CharField(max_length=50, null=True, blank=True)
    transfer_certificate = models.FileField(upload_to="tc/", null=True, blank=True)

    current_unit = models.CharField(max_length=100, null=True, blank=True)
    parent_unit = models.CharField(max_length=100, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)


    is_active = models.BooleanField(default=False)
    index_no = models.PositiveIntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.user.email


# ----------------------------
# STUDENT TYPE
# ----------------------------
class StudentType(BaseModel):

    name = models.CharField(max_length=150)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# ----------------------------
# STUDENT GROUP
# ----------------------------
class StudentGroup(BaseModel):

    name = models.CharField(max_length=150, unique=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

 

# ----------------------------
# ACTIVITY
# ----------------------------
class Activity(BaseModel):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    activity_date = models.DateField()
    activity = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.email} - {self.activity_date}"


# ----------------------------
# SPOUSE
# ----------------------------
class Spouse(BaseModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    spouse_name = models.CharField(max_length=150)
    spouse_phone = models.CharField(max_length=20, blank=True, null=True)
    spouse_address = models.TextField(blank=True, null=True)
    spouse_profession = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.spouse_name


# ----------------------------
# QUALIFICATION
# ----------------------------
class Qualification(BaseModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE,  blank=True, null=True, related_name="qualifications")

    name = models.CharField(max_length=150)
    qualification_type = models.CharField(
        max_length=10,
        choices=QualificationType.choices,
        default=QualificationType.CIVIL
    )

    institute = models.CharField(max_length=150)

    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

    result = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.institute}"


# ----------------------------
# BANK ACCOUNT
# ----------------------------
class BankAccount(BaseModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True,related_name="bank_accounts")

    bank_name = models.CharField(max_length=150)
    account_number = models.CharField(max_length=100)
    branch = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


# ----------------------------
# MILITARY QUALIFICATION
# ----------------------------
class MilitaryQualification(BaseModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE,  blank=True, null=True,related_name="military_qualifications")

    cadre_name = models.CharField(max_length=150)
    level = models.CharField(max_length=100)
    institute = models.CharField(max_length=150, blank=True, null=True)

    duration_from = models.DateField(null=True, blank=True)
    duration_to = models.DateField(null=True, blank=True)

    result = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.cadre_name} - {self.level}"


# ----------------------------
# SERVICE RECORD
# ----------------------------
class ServiceRecord(BaseModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    institution = models.CharField(max_length=150)
    appointment = models.CharField(max_length=150, blank=True, null=True)

    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.full_name} - {self.institution}"


# ----------------------------
# AWARD
# ----------------------------
class Award(BaseModel):

    decoration = models.CharField(max_length=150)
    receipt_date = models.DateField(null=True, blank=True)
    purpose = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.decoration


# ----------------------------
# UN MISSION
# ----------------------------
class UNMission(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True, related_name="un_missions")
    mission_name = models.CharField(max_length=150)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

    appointment = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.mission_name


# ----------------------------
# COUNTRY VISITED
# ----------------------------
class CountryVisited(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True, related_name="visited_country")
    country = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()

    purpose = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.country


class BatchMembership(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name="batch_memberships")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True, blank=True)

    # extra tracking fields
    joined_at = models.DateField(auto_now_add=True)
    left_at = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    index_no = models.PositiveIntegerField(null=True,blank=True)
 
    class Meta:
        constraints = [

            # same student + same batch not allowed
            models.UniqueConstraint(
                fields=['student', 'batch'],
                name='unique_batch_per_student'
            ),

            # only one NULL batch per student
            models.UniqueConstraint(
                fields=['student'],
                condition=Q(batch__isnull=True),
                name='unique_null_batch_per_student'
            ),

            # same batch -> unique index_no
            models.UniqueConstraint(
                fields=['batch', 'index_no'],
                name='unique_index_no_per_batch'
            )
        ]

    def save(self, *args, **kwargs):

        # auto set left_at from batch_end
        if self.batch and self.batch.batch_end:
            self.left_at = self.batch.batch_end

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.batch}"