from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    SubjectViewSet,
    ModuleViewSet,
    SyllabusViewSet, 
    BatchViewSet
)

router = DefaultRouter()

# -----------------------
# Routes
# -----------------------
router.register(r"courses", CourseViewSet)
router.register(r"subjects", SubjectViewSet)
router.register(r"modules", ModuleViewSet)
router.register(r"syllabus", SyllabusViewSet) 
router.register(r"batches", BatchViewSet)

app_name = "courses"
urlpatterns = [
    path("", include(router.urls)),
    
]