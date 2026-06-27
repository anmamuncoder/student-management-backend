from django.db import models
from django.core.exceptions import ValidationError

from apps.course.models import Course,Batch,Module,Subject
from apps.student.models import BatchMembership, Student
from .constants import METHOD_CHOICES,  GRADE_TYPE_CHOICES, AttendanceStatus
from kernel.models import BaseModel
from apps.accounts.models import User

# -------------------------
# Grading System
# -------------------------
class ExamGrade(BaseModel):

    b_side_grade = models.CharField(max_length=20)
    y_side_grade = models.CharField(max_length=20)

    grade_point = models.FloatField(null=True, blank=True)

    mark_from = models.PositiveIntegerField()
    mark_to = models.PositiveIntegerField()

    note = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ["mark_from"]


    def __str__(self):
        grade = self.b_side_grade or "No Grade"
        return f"{grade} ({self.mark_from}-{self.mark_to})"


# -------------------------
# Exam 
# -------------------------
class Exam(BaseModel):
    name = models.CharField(max_length=255,null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="exams")

    exam_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    room_no = models.CharField(max_length=50, null=True, blank=True)
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPE_CHOICES,null=True, blank=True)

    note = models.TextField(blank=True, null=True)
    examiner =  models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="examiner_exams")

    is_attendance_locked = models.BooleanField(default=False)

    @property
    def total_present(self):
        return self.results.filter(status=AttendanceStatus.PRESENT).count()

    @property
    def total_absent(self):
        return self.results.filter(status=AttendanceStatus.ABSENT).count()


    class Meta:

        ordering = [
            "-exam_date",
            "start_time",
        ]

    @property
    def batch(self):
        if (self.subject and self.subject.module):
            return self.subject.module.batch
        return None

 

# -------------------------
# Exam Result
# -------------------------
class ExamResult(BaseModel):
    membership = models.ForeignKey(BatchMembership,on_delete=models.CASCADE,related_name="exam_results",null=True, blank=True)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,related_name="results")
    status = models.CharField(max_length=20,choices=AttendanceStatus.choices,default=AttendanceStatus.PENDING)

    obtained_marks = models.FloatField(null=True,blank=True)
    remarks = models.TextField(null=True, blank=True)
    
    attended_at = models.DateTimeField(auto_now_add=True,null=True, blank=True) 



    @property
    def full_mark(self):
        """
        Subject - WeightageDistribution.full_mark
        """
        try:
            return self.exam.subject.weightage_distribution.full_mark
        except AttributeError:
            return 0
        
    @property
    def wt(self):
        try:
            return self.exam.subject.weightage_distribution.wt
        except AttributeError:
            return 0


    @property
    def obtained_marks_percentage(self):
        """
        Obtained mark - percentage
        """
        try:
            full_mark = self.exam.subject.weightage_distribution.full_mark

            if not full_mark or self.obtained_marks is None:
                return 0

            return round((self.obtained_marks / full_mark) * 100, 2)

        except AttributeError:
            return 0
        
    @property
    def wt_marks(self):
        """
        Example:
        Full Mark = 100
        Obtained = 67
        WT = 7

        Result = (67 / 100) * 7 = 4.69
        """
        try:
            wd = self.exam.subject.weightage_distribution

            if wd.full_mark <= 0 or self.obtained_marks is None:
                return 0

            return round((self.obtained_marks / wd.full_mark) * wd.wt, 2)

        except AttributeError:
            return 0
        
    @property
    def pass_mark(self):
        try:
            return self.exam.subject.weightage_distribution.pass_mark
        except AttributeError:
            return 0

    @property
    def is_passed(self):
        try:
            return (
                self.obtained_marks is not None
                and self.obtained_marks >= self.pass_mark
            )
        except Exception:
            return False



    @property
    def grade(self):
        """
        Returns the matching ExamGrade object.
        """
        try:
            return ExamGrade.objects.filter(
                mark_from__lte=self.obtained_marks_percentage,
                mark_to__gte=self.obtained_marks_percentage
            ).first()
        except Exception:
            return None


    @property
    def b_side_grade(self):
        """
        B-side grade.
        """
        grade = self.grade
        return grade.b_side_grade if grade else None

    @property
    def y_side_grade(self):
        """
        Y-side grade.
        """
        grade = self.grade
        return grade.y_side_grade if grade else None


    @property
    def grade_point(self):
        """
        Grade point based on obtained percentage.
        """
        grade = self.grade
        return grade.grade_point if grade else 0

    @property
    def merit_position(self):
        """
        Returns merit rank within the same exam.
        Highest marks = Rank 1
        Tie-breaker = membership index_no (asc)
        """

        if self.obtained_marks is None:
            return None

        # count how many students are better than this student
        better_count = ExamResult.objects.filter(
            exam=self.exam
        ).filter(
            models.Q(obtained_marks__gt=self.obtained_marks) |
            models.Q(
                obtained_marks=self.obtained_marks,
                membership__index_no__lt=self.membership.index_no
            )
        ).count()

        return better_count + 1

    class Meta:

        ordering = [
            "membership__batch__name",
            "membership__index_no"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["membership", "exam"],
                name="unique_exam_result_per_student"
            )
        ]
        indexes = [
            models.Index(fields=["exam"]),
            models.Index(fields=["membership"]),
            models.Index(fields=["status"]),
            models.Index(fields=["exam", "status"]),
        ]

    def clean(self):
        if (self.membership and self.exam and self.exam.batch):
            if self.membership.batch != self.exam.batch:
                raise ValidationError("Student batch and exam batch do not match.")

    def save(self, *args, **kwargs):
        if self.status == AttendanceStatus.ABSENT:
            self.obtained_marks = 0

        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return (f"{self.membership.student} " f"- " f"{self.exam}")