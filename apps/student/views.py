from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import (
    Student, StudentType, StudentGroup, Activity,
    Spouse, Qualification, BankAccount,
    MilitaryQualification, ServiceRecord,
    Award, UNMission, CountryVisited
)

from .serializers import (
    StudentSerializer, StudentTypeSerializer, StudentGroupSerializer,
    ActivitySerializer, SpouseSerializer, QualificationSerializer,
    BankAccountSerializer, MilitaryQualificationSerializer,
    ServiceRecordSerializer, AwardSerializer,
    UNMissionSerializer, CountryVisitedSerializer
)

# ----------------------------
# Base View (optional reuse)
# ----------------------------
class BaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]


# ----------------------------
# Student Type
# ----------------------------
class StudentTypeViewSet(BaseViewSet):
    queryset = StudentType.objects.all()
    serializer_class = StudentTypeSerializer


# ----------------------------
# Student Group
# ----------------------------
class StudentGroupViewSet(BaseViewSet):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer


# ----------------------------
# Student
# ----------------------------
class StudentViewSet(BaseViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# ----------------------------
# Activity
# ----------------------------
class ActivityViewSet(BaseViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


# ----------------------------
# Spouse
# ----------------------------
class SpouseViewSet(BaseViewSet):
    queryset = Spouse.objects.all()
    serializer_class = SpouseSerializer


# ----------------------------
# Qualification
# ----------------------------
class QualificationViewSet(BaseViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


# ----------------------------
# Bank Account
# ----------------------------
class BankAccountViewSet(BaseViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


# ----------------------------
# Military Qualification
# ----------------------------
class MilitaryQualificationViewSet(BaseViewSet):
    queryset = MilitaryQualification.objects.all()
    serializer_class = MilitaryQualificationSerializer


# ----------------------------
# Service Record
# ----------------------------
class ServiceRecordViewSet(BaseViewSet):
    queryset = ServiceRecord.objects.all()
    serializer_class = ServiceRecordSerializer


# ----------------------------
# Award
# ----------------------------
class AwardViewSet(BaseViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer


# ----------------------------
# UN Mission
# ----------------------------
class UNMissionViewSet(BaseViewSet):
    queryset = UNMission.objects.all()
    serializer_class = UNMissionSerializer


# ----------------------------
# Country Visited
# ----------------------------
class CountryVisitedViewSet(BaseViewSet):
    queryset = CountryVisited.objects.all()
    serializer_class = CountryVisitedSerializer