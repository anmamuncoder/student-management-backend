from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import (
    Student, StudentType, StudentGroup, Activity,
    Spouse, Qualification, BankAccount,
    MilitaryQualification, ServiceRecord,
    Award, UNMission, CountryVisited, BatchMembership
)

from .serializers import (
    StudentSerializer, StudentTypeSerializer, StudentGroupSerializer,
    ActivitySerializer, SpouseSerializer, QualificationSerializer,
    BankAccountSerializer, MilitaryQualificationSerializer,
    ServiceRecordSerializer, AwardSerializer,
    UNMissionSerializer, CountryVisitedSerializer, BatchMembershipSerializer
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
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = StudentSerializer
    


# ----------------------------
# Batch Membership
# ----------------------------
class BatchMembershipViewSet(BaseViewSet):
    # queryset = BatchMembership.objects.filter(
    #     Q(left_at__isnull=True) | Q(left_at__gt=timezone.now())
    #     ).order_by('-created_at')
    queryset = BatchMembership.objects.all().order_by('-created_at')

    serializer_class = BatchMembershipSerializer
    
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