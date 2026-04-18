from rest_framework.serializers import ModelSerializer
from .models import Course, Subject, Module, Syllabus, DetailSyllabus, Batch


# -----------------------
# Detail Syllabus
# -----------------------
class DetailSyllabusSerializer(ModelSerializer):
    class Meta:
        model = DetailSyllabus
        fields = "__all__"


# -----------------------
# Subject
# -----------------------
class SubjectSerializer(ModelSerializer):
    detail_syllabus = DetailSyllabusSerializer(many=True,read_only=True)
    class Meta:
        model = Subject
        fields = "__all__"



# -----------------------
# Syllabus
# -----------------------
class SyllabusSerializer(ModelSerializer):
    class Meta:
        model = Syllabus
        fields = "__all__"


# -----------------------
# Module
# -----------------------
class ModuleSerializer(ModelSerializer):
    syllabus_blocks = SyllabusSerializer(many=True,read_only=True)
    detail_syllabus = DetailSyllabusSerializer(many=True,read_only=True)

    class Meta:
        model = Module
        fields = "__all__"


# -----------------------
# Batch
# -----------------------
class BatchSerializer(ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"


# -----------------------
# Course
# -----------------------
class CourseSerializer(ModelSerializer):
    syllabus_blocks = SyllabusSerializer(many=True, read_only=True)
    detail_syllabus = DetailSyllabusSerializer(many=True,read_only=True)
    batches = BatchSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


        