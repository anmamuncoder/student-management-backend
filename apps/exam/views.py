from rest_framework import viewsets
from .models import ExamGrade, ExamSchedule, Exam, ExamAttendance
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ExamGradeSerializer,
    ExamScheduleSerializer,
    ExamSerializer,
    ExamAttendanceSerializer,
)
from kernel.viewsets import BaseViewSet


class ExamGradeViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ExamGrade.objects.all()
    serializer_class = ExamGradeSerializer


class ExamScheduleViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ExamSchedule.objects.all().order_by("-exam_date")
    serializer_class = ExamScheduleSerializer


class ExamViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class ExamAttendanceViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ExamAttendance.objects.all()
    serializer_class = ExamAttendanceSerializer

    