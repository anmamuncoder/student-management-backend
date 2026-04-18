from rest_framework import viewsets
from .models import GovtHoliday, TrainingSchedule
from .serializers import GovtHolidaySerializer, TrainingScheduleSerializer
from rest_framework.permissions import IsAuthenticated


# -------------------------
# Govt Holiday ViewSet
# -------------------------
class GovtHolidayViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = GovtHoliday.objects.all().order_by("-start_date")
    serializer_class = GovtHolidaySerializer


# -------------------------
# Training Schedule ViewSet
# -------------------------
class TrainingScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = TrainingSchedule.objects.all().order_by("-start_date")
    serializer_class = TrainingScheduleSerializer

    