from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Course, Subject, Module, Syllabus, Batch
from .serializers import (
    CourseSerializer,
    SubjectSerializer,
    ModuleSerializer,
    SyllabusSerializer,
    BatchSerializer
)


class BaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]


# -----------------------
# Course
# -----------------------
class CourseViewSet(BaseViewSet):
    queryset = Course.objects.prefetch_related("syllabus_blocks__module","children").order_by('-created_at')
    serializer_class = CourseSerializer


# -----------------------
# Subject
# -----------------------
class SubjectViewSet(BaseViewSet):
    queryset = Subject.objects.all().order_by('-created_at')
    serializer_class = SubjectSerializer


# -----------------------
# Module
# -----------------------
class ModuleViewSet(BaseViewSet):
    queryset = Module.objects.all().order_by('-created_at')
    serializer_class = ModuleSerializer


# -----------------------
# Syllabus
# -----------------------
class SyllabusViewSet(BaseViewSet):
    queryset = Syllabus.objects.all().order_by('-created_at')
    serializer_class = SyllabusSerializer


# -----------------------
# Batch
# -----------------------
class BatchViewSet(BaseViewSet):
    queryset = Batch.objects.all().order_by('-created_at')
    serializer_class = BatchSerializer