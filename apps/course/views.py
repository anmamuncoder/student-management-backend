from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Course, Subject, Module, Syllabus, DetailSyllabus, Batch
from .serializers import (
    CourseSerializer,
    SubjectSerializer,
    ModuleSerializer,
    SyllabusSerializer,
    DetailSyllabusSerializer,
    BatchSerializer
)


class BaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]


# -----------------------
# Course
# -----------------------
class CourseViewSet(BaseViewSet):
    queryset = Course.objects.prefetch_related("syllabus_blocks__module","children")
    serializer_class = CourseSerializer


# -----------------------
# Subject
# -----------------------
class SubjectViewSet(BaseViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# -----------------------
# Module
# -----------------------
class ModuleViewSet(BaseViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


# -----------------------
# Syllabus
# -----------------------
class SyllabusViewSet(BaseViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer


# -----------------------
# Detail Syllabus
# -----------------------
class DetailSyllabusViewSet(BaseViewSet):
    queryset = DetailSyllabus.objects.all()
    serializer_class = DetailSyllabusSerializer


# -----------------------
# Batch
# -----------------------
class BatchViewSet(BaseViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer