from rest_framework import serializers
from .models import GovtHoliday, TrainingSchedule


# -------------------------
# Govt Holiday Serializer
# -------------------------
class GovtHolidaySerializer(serializers.ModelSerializer):
    total_days = serializers.ReadOnlyField()

    class Meta:
        model = GovtHoliday
        fields = "__all__"


# -------------------------
# Training Schedule Serializer
# -------------------------
class TrainingScheduleSerializer(serializers.ModelSerializer): 

    class Meta:
        model = TrainingSchedule
        fields = "__all__"

    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("Start date must be before end date")
        return data
    
    