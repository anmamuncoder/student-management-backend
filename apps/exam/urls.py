from rest_framework.routers import DefaultRouter
from .views import (
    ExamGradeViewSet,
    ExamScheduleViewSet,
    ExamViewSet,
    ExamAttendanceViewSet,
)

router = DefaultRouter()

router.register(r"exam-grades", ExamGradeViewSet)
router.register(r"exam-schedules", ExamScheduleViewSet)
router.register(r"exams", ExamViewSet)
router.register(r"exam-attendance", ExamAttendanceViewSet)

app_name = "exams"
urlpatterns = router.urls

