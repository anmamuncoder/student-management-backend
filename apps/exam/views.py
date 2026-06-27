from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.db.models import F

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import (
    IsAuthenticated
)

from .constants import AttendanceStatus

from .models import (
    ExamGrade,
    Exam,
    ExamResult,
)

from .serializers import (
    ExamGradeSerializer,
    ExamSerializer,
    ExamResultSerializer,
    ExamHistorySerializer
)

from .filters import (
    ExamFilter,
    ExamResultFilter,
)

from .services import create_exam_result

from kernel.viewsets import BaseViewSet
from .permissions import IsExaminerOrAdminOrReadOnly


from apps.student.models import BatchMembership
from apps.student.serializers import BatchMembershipSerializer


class ExamGradeViewSet(BaseViewSet):

    permission_classes = [IsAuthenticated]

    queryset = ExamGrade.objects.all().order_by('-grade_point')

    serializer_class = ExamGradeSerializer


class ExamViewSet(BaseViewSet):

    permission_classes = [IsAuthenticated]

    queryset = Exam.objects.select_related(
        "subject",
        "subject__module",
        "subject__module__batch",
    ).order_by('-created_at')

    serializer_class = ExamSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_class = ExamFilter

    def perform_create(self, serializer):

        exam = serializer.save()
        create_exam_result(exam)


    @action(detail=True, methods=["post"])
    def lock_attendance(self, request, pk=None):
        exam = self.get_object()

        if exam.is_attendance_locked:
            return Response({"detail": "Attendance is already locked."},status=status.HTTP_400_BAD_REQUEST,)

        exam.is_attendance_locked = True
        exam.save(update_fields=["is_attendance_locked"])

        return Response({"detail": "Attendance locked successfully."},status=status.HTTP_200_OK,)

    @action(detail=True, methods=["post"])
    def unlock_attendance(self, request, pk=None):
        exam = self.get_object()
        user = request.user

        is_admin = (user.is_superuser or user.user_roles.filter(role__slug="admin").exists())

        if not is_admin:
            return Response(
                {
                    "detail": "Only admin users can unlock attendance."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not exam.is_attendance_locked:
            return Response(
                {
                    "detail": "Attendance is already unlocked."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        exam.is_attendance_locked = False
        exam.save(update_fields=["is_attendance_locked"])

        return Response(
            {
                "detail": "Attendance unlocked successfully."
            },
            status=status.HTTP_200_OK,
        )


class ExamResultViewSet(BaseViewSet):

    permission_classes = [IsAuthenticated,IsExaminerOrAdminOrReadOnly] 

    queryset = ExamResult.objects.select_related(
        "membership",
        "membership__student",
        "membership__student__user",
        "membership__batch",
        "exam",
        "exam__subject",
    ).order_by("membership__index_no")
 
    serializer_class = ExamResultSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_class = ExamResultFilter

    @action(
        detail=False,
        methods=["post"],
        url_path="all-status"
    )
    @transaction.atomic
    def all_status(self, request):

        exam_id = request.query_params.get("exam")
        batch_id = request.query_params.get("batch")
        attendance_status = request.data.get("status")

        if not exam_id:
            return Response(
                {
                    "status": False,
                    "message": "exam is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not batch_id:
            return Response(
                {
                    "status": False,
                    "message": "batch is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_statuses = [
            AttendanceStatus.PRESENT,
            AttendanceStatus.ABSENT,
            AttendanceStatus.LATE,
            AttendanceStatus.LEAVE,
        ]

        if attendance_status not in valid_statuses:
            return Response(
                {
                    "status": False,
                    "message": "Invalid status"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_count = ExamResult.objects.filter(
            exam_id=exam_id,
            membership__batch_id=batch_id,
        ).update(
            status=attendance_status
        )

        return Response(
            {
                "status": True,
                "updated_count": updated_count
            }
        )
 

class ExamHistoryViewSet(BaseViewSet):

    serializer_class = ExamHistorySerializer
    queryset = BatchMembership.objects.select_related(
        "student",
        "student__user",
        "batch",
    ).order_by("index_no")

    def retrieve(self, request, *args, **kwargs):

        batch_id = kwargs.get("pk")

        queryset = (
            self.get_queryset()
            .filter(batch_id=batch_id)
        )

        serializer = self.get_serializer(
            queryset,
            many=True,
            context={
                "grade_type": request.query_params.get("grade_type")
            }
        )

        return Response(serializer.data)