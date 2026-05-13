from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, NoticeViewSet


router = DefaultRouter()

router.register(r"events", EventViewSet, basename="events")
router.register(r"notices", NoticeViewSet, basename="notices")

app_name = "noticeboards"
urlpatterns = [
    path("", include(router.urls)),
]