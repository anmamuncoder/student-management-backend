from rest_framework import viewsets
from .models import ExamGrade, ExamSchedule, Exam, ExamAttendance
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ExamGradeSerializer,
    ExamScheduleSerializer,
    ExamSerializer,
    ExamAttendanceSerializer,
)


class ExamGradeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ExamGrade.objects.all()
    serializer_class = ExamGradeSerializer


class ExamScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ExamSchedule.objects.all().order_by("-exam_date")
    serializer_class = ExamScheduleSerializer


class ExamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class ExamAttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ExamAttendance.objects.all()
    serializer_class = ExamAttendanceSerializer