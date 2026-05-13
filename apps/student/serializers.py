from rest_framework.serializers import ModelSerializer
from .models import Student, StudentType, StudentGroup, Activity, Spouse, Qualification, BankAccount, MilitaryQualification, ServiceRecord, Award, UNMission, CountryVisited, BatchMembership


# ----------------------------
# Student Type
# ----------------------------
class StudentTypeSerializer(ModelSerializer):
    class Meta:
        model = StudentType
        fields = "__all__"


# ----------------------------
# Student Group
# ----------------------------
class StudentGroupSerializer(ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = "__all__"


# ----------------------------
# Student
# ----------------------------
class SampleStudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


# ----------------------------
# Batch Membership
# ----------------------------
class BatchMembershipSerializer(ModelSerializer):
    student_details = SampleStudentSerializer(source='student', read_only=True)
    
    class Meta:
        model = BatchMembership
        fields = "__all__"


# ----------------------------
# Activity
# ----------------------------
class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"


# ----------------------------
# Spouse
# ----------------------------
class SpouseSerializer(ModelSerializer):
    class Meta:
        model = Spouse
        fields = "__all__"


# ----------------------------
# Qualification
# ----------------------------
class QualificationSerializer(ModelSerializer):
    class Meta:
        model = Qualification
        fields = "__all__"


# ----------------------------
# Bank Account
# ----------------------------
class BankAccountSerializer(ModelSerializer):
    class Meta:
        model = BankAccount
        fields = "__all__"


# ----------------------------
# Military Qualification
# ----------------------------
class MilitaryQualificationSerializer(ModelSerializer):
    class Meta:
        model = MilitaryQualification
        fields = "__all__"


# ----------------------------
# Service Record
# ----------------------------
class ServiceRecordSerializer(ModelSerializer):
    class Meta:
        model = ServiceRecord
        fields = "__all__"


# ----------------------------
# Award
# ----------------------------
class AwardSerializer(ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"


# ----------------------------
# UN Mission
# ----------------------------
class UNMissionSerializer(ModelSerializer):
    class Meta:
        model = UNMission
        fields = "__all__"


# ----------------------------
# Country Visited
# ----------------------------
class CountryVisitedSerializer(ModelSerializer):
    class Meta:
        model = CountryVisited
        fields = "__all__"


# ----------------------------
# Student
# ----------------------------
class StudentSerializer(ModelSerializer):

    student_type_details = StudentTypeSerializer(
        source='student_type',
        read_only=True
    )

    qualifications = QualificationSerializer(
        many=True,
        read_only=True
    )

    bank_accounts = BankAccountSerializer(
        many=True,
        read_only=True
    )

    military_qualifications = MilitaryQualificationSerializer(
        many=True,
        read_only=True
    )

    un_missions = UNMissionSerializer(
        many=True,
        read_only=True
    )

    visited_country = CountryVisitedSerializer(
        many=True,
        read_only=True
    )

    batch_memberships = BatchMembershipSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Student
        fields = "__all__"