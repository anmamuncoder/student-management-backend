from rest_framework.routers import DefaultRouter
from .views import GovtHolidayViewSet, TrainingScheduleViewSet

router = DefaultRouter()

router.register(r"govt-holidays", GovtHolidayViewSet, basename="govt-holiday")
router.register(r"training-schedules", TrainingScheduleViewSet, basename="training-schedule")

app_name = "time_tables"
urlpatterns = router.urls