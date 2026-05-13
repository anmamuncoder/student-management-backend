from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import (
    TrainingProgramme,
    WeightageDistribution,
    ObservationSheet,
    FinalResult
)

from .serializers import (
    TrainingProgrammeSerializer,
    WeightageDistributionSerializer,
    ObservationSheetSerializer,
    FinalResultSerializer
) 

from kernel.viewsets import BaseViewSet


class TrainingProgrammeViewSet(BaseViewSet):
    queryset = TrainingProgramme.objects.all()
    serializer_class = TrainingProgrammeSerializer


class WeightageDistributionViewSet(BaseViewSet):
    queryset = WeightageDistribution.objects.all()
    serializer_class = WeightageDistributionSerializer


class FinalResultViewSet(BaseViewSet):
    queryset = FinalResult.objects.all()
    serializer_class = FinalResultSerializer


class ObservationSheetViewSet(BaseViewSet):
    queryset = ObservationSheet.objects.all()
    serializer_class = FinalResultSerializer