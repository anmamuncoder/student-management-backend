from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StudentViewSet, StudentTypeViewSet, StudentGroupViewSet,
    ActivityViewSet, SpouseViewSet, QualificationViewSet,
    BankAccountViewSet, MilitaryQualificationViewSet,
    ServiceRecordViewSet, AwardViewSet,
    UNMissionViewSet, CountryVisitedViewSet
)

router = DefaultRouter()

# ----------------------------
# Register routes
# ----------------------------
router.register(r"students", StudentViewSet)
router.register(r"student-types", StudentTypeViewSet)
router.register(r"student-groups", StudentGroupViewSet)

router.register(r"activities", ActivityViewSet)
router.register(r"spouses", SpouseViewSet)
router.register(r"qualifications", QualificationViewSet)
router.register(r"bank-accounts", BankAccountViewSet)
router.register(r"military-qualifications", MilitaryQualificationViewSet)
router.register(r"service-records", ServiceRecordViewSet)
router.register(r"awards", AwardViewSet)
router.register(r"un-missions", UNMissionViewSet)
router.register(r"countries-visited", CountryVisitedViewSet)

app_name = "students"
urlpatterns = [
    path("", include(router.urls)),
    
]