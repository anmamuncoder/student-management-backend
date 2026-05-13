from rest_framework.serializers import ModelSerializer
from .models import (
    TrainingProgramme,
    WeightageDistribution,
    ObservationSheet,
    FinalResult
)

class TrainingProgrammeSerializer(ModelSerializer):
    class Meta:
        model = TrainingProgramme
        fields = "__all__"

class WeightageDistributionSerializer(ModelSerializer):
    class Meta:
        model = WeightageDistribution
        fields = "__all__"

class FinalResultSerializer(ModelSerializer):
    class Meta:
        model = FinalResult
        fields = "__all__"

class ObservationSheetSerializer(ModelSerializer):
    class Meta:
        model = ObservationSheet
        fields = "__all__"

    