import django_filters

from .models import Exam, ExamResult


class ExamFilter(django_filters.FilterSet):

    batch = django_filters.UUIDFilter(field_name="subject__module__batch__id")
    subject = django_filters.UUIDFilter(field_name="subject__id")
    exam_date = django_filters.DateFilter(field_name="exam_date")

    class Meta:
        model = Exam

        fields = [
            "batch",
            "subject",
            "exam_date",
        ]


class ExamResultFilter(django_filters.FilterSet):

    batch = django_filters.UUIDFilter(field_name="membership__batch__id")
    exam = django_filters.UUIDFilter(field_name="exam__id")
    student = django_filters.UUIDFilter(field_name="membership__student__id")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = ExamResult

        fields = [
            "batch",
            "exam",
            "student",
            "status",
        ]