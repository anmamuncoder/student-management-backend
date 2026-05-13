from rest_framework.routers import DefaultRouter
from .views import (
    TrainingProgrammeViewSet,
    WeightageDistributionViewSet,
    ObservationSheetViewSet,
    FinalResultViewSet
)

router = DefaultRouter()

router.register(r"training-programmes", TrainingProgrammeViewSet)
router.register(r"weightage-distributions", WeightageDistributionViewSet)
router.register(r"observation-sheets", ObservationSheetViewSet)
router.register(r"final-results", FinalResultViewSet)

app_name = "trainings"

urlpatterns = router.urls