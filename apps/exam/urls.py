from rest_framework.routers import DefaultRouter
from .views import (
    ExamGradeViewSet,
    ExamViewSet,
    ExamViewSet,
    ExamResultViewSet,
    ExamHistoryViewSet
)

router = DefaultRouter()

router.register(r"exam-grades", ExamGradeViewSet)
router.register(r"exams", ExamViewSet) 
router.register(r"exam-results", ExamResultViewSet)
router.register(r"exam-history", ExamHistoryViewSet)

app_name = "exams"
urlpatterns = router.urls

