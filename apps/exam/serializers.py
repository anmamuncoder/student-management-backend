from rest_framework import serializers
from .models import ExamGrade, ExamSchedule, Exam, ExamAttendance


# -------------------------
# Exam Grade
# -------------------------
class ExamGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamGrade
        fields = "__all__"


# -------------------------
# Exam Schedule
# -------------------------
class ExamScheduleSerializer(serializers.ModelSerializer):   
    class Meta:
        model = ExamSchedule
        fields = "__all__"

    def validate(self, data):
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError("Start time must be before end time")
        return data


# -------------------------
# Exam
# -------------------------
class ExamSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Exam
        fields = "__all__"


# -------------------------
# Exam Attendance
# -------------------------
class ExamAttendanceSerializer(serializers.ModelSerializer): 

    class Meta:
        model = ExamAttendance
        fields = "__all__"

