from rest_framework.serializers import ModelSerializer
from .models import Course, Subject, Module, Syllabus, DetailSyllabus, Batch


# -----------------------
# Subject
# -----------------------
class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


# -----------------------
# Module
# -----------------------
class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


# -----------------------
# Syllabus
# -----------------------
class SyllabusSerializer(ModelSerializer):
    class Meta:
        model = Syllabus
        fields = "__all__"


# -----------------------
# Detail Syllabus
# -----------------------
class DetailSyllabusSerializer(ModelSerializer):
    class Meta:
        model = DetailSyllabus
        fields = "__all__"


# -----------------------
# Course
# -----------------------
class CourseSerializer(ModelSerializer):
    syllabus_blocks = SyllabusSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = "__all__"


# -----------------------
# Batch
# -----------------------
class BatchSerializer(ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"
        