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
    queryset = TrainingProgramme.objects.all().order_by('-created_at')
    serializer_class = TrainingProgrammeSerializer
    permission_classes = [IsAuthenticated]



class WeightageDistributionViewSet(BaseViewSet):
    queryset = WeightageDistribution.objects.all().order_by('-created_at')
    serializer_class = WeightageDistributionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Superuser can access all
        if user.is_superuser:
            return WeightageDistribution.objects.all().order_by('-created_at')

        # Admin role users can access all
        is_admin = user.user_roles.filter(role__name__iexact='admin').exists()

        if is_admin:
            return WeightageDistribution.objects.all().order_by('-created_at')

        # Normal users can access only their own observations
        return WeightageDistribution.objects.filter(
            observation_by=user
        ).order_by('-created_at')


class FinalResultViewSet(BaseViewSet):
    queryset = FinalResult.objects.all().order_by('-created_at')
    serializer_class = FinalResultSerializer
    permission_classes = [IsAuthenticated]


class ObservationSheetViewSet(BaseViewSet):
    queryset = ObservationSheet.objects.all().order_by('-created_at')
    serializer_class = ObservationSheetSerializer
    permission_classes = [IsAuthenticated]
