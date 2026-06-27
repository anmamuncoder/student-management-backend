from rest_framework import serializers

from .models import (
    ExamGrade,
    Exam,
    ExamResult,
)
from apps.training.serializers import WeightageDistributionSerializer
from apps.student.serializers import SampleStudentSerializer
from apps.student.models import BatchMembership, Student
from apps.course.models import Module
from .services import ModuleExamService
from .constants import GRADE_TYPE_CHOICES

# -------------------------
# Exam Grade
# -------------------------
class ExamGradeSerializer(serializers.ModelSerializer):



    class Meta:
        model = ExamGrade
        fields = "__all__"

# -------------------------
# Exam
# -------------------------
class ExamSerializer(serializers.ModelSerializer):

    total_present = serializers.IntegerField(read_only=True)
    total_absent = serializers.IntegerField(read_only=True)

    subject_name = serializers.CharField(source="subject.name",read_only=True)
    # module_name = serializers.CharField(source="subject.module.name",read_only=True)


    class Meta:
        model = Exam
        fields = "__all__"
        read_only_fields = ["is_result_locked",  "total_present","total_absent",]

    def validate(self, data):

        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if start_time and end_time:

            if start_time >= end_time:

                raise serializers.ValidationError(
                    "Start time must be before end time"
                )

        return data

# -------------------------
# Exam Result
# -------------------------
class ExamResultSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    # Membership Details
    membership_index_no = serializers.IntegerField(source="membership.index_no",read_only=True)
    membership_is_active = serializers.BooleanField(source="membership.is_active",read_only=True)

    # Student Details
    student_id = serializers.UUIDField(source="membership.student.id",read_only=True)

    student_name = serializers.CharField(source="membership.student.user.full_name",read_only=True)
    student_phone = serializers.CharField(source="membership.student.user.phone",read_only=True)
    student_personal_number = serializers.CharField(source="membership.student.user.personal_number",read_only=True)
    student_email = serializers.EmailField(source="membership.student.user.email",read_only=True)
    student_photo = serializers.ImageField(source="membership.student.user.photo",read_only=True)
    student_current_unit = serializers.CharField(source="membership.student.user.current_unit",read_only=True)
    student_rank = serializers.CharField(source="membership.student.user.rank.name",read_only=True)

    # Batch Details
    batch_id = serializers.UUIDField(source="membership.batch.id",read_only=True)

    batch_name = serializers.CharField(source="membership.batch.name",read_only=True)

    # Exam Details
    exam_name = serializers.CharField(source="exam.name",read_only=True)
    exam_date = serializers.DateField(source="exam.exam_date",read_only=True)
    subject_name = serializers.CharField(source="exam.subject.name",read_only=True)

    subject_weightage_distribution = WeightageDistributionSerializer(source="exam.subject.weightage_distribution",read_only=True)   

    result_analysis = serializers.SerializerMethodField()

    class Meta:
        model = ExamResult
        fields = "__all__"

    def get_result_analysis(self, obj):
        return {
            "full_mark": obj.full_mark,
            "pass_mark": obj.pass_mark,
            
            "obtained_marks_percentage": obj.obtained_marks_percentage,
            "wt_marks": obj.wt_marks,

            "is_passed": obj.is_passed,

            "b_side_grade": obj.b_side_grade,
            "y_side_grade": obj.y_side_grade,
            "grade_point": obj.grade_point,

            "merit_position": obj.merit_position,
        }
    
    
    def validate(self, attrs):

        membership = attrs.get(
            "membership",
            getattr(self.instance, "membership", None)
        )

        exam = attrs.get(
            "exam",
            getattr(self.instance, "exam", None)
        )

        # Batch validation
        if membership and exam and exam.batch:
            if membership.batch != exam.batch:
                raise serializers.ValidationError(
                    "Student batch and exam batch do not match."
                )

        request = self.context.get("request")
        user = request.user if request else None

        is_admin = (
            user and (
                user.is_superuser
                or user.user_roles.filter(role__slug="admin").exists()
            )
        )

        # Attendance lock validation
        if (
            not is_admin
            and self.instance
            and "status" in attrs
            and self.instance.exam.is_attendance_locked
        ):
            raise serializers.ValidationError({
                "status": "Attendance has been locked for this exam."
            })

        return attrs


# ----------------------------
# Exam History
# ----------------------------
# class ExamHistorySerializer(serializers.ModelSerializer):
#     student_details = SampleStudentSerializer(source='student', read_only=True)
#     exams = serializers.SerializerMethodField()

#     class Meta:
#         model = BatchMembership
#         fields = "__all__"

#     def get_exams(self, obj):
#         exams = Exam.objects.filter(
#             subject__module__batch=obj.batch
#         ).distinct()

#         data = []

#         for exam in exams:
#             exam_data = ExamSerializer(exam).data

#             exam_result = ExamResult.objects.filter(
#                 membership=obj,
#                 exam=exam
#             ).first()

#             if exam_result:
#                 result_data = ExamResultSerializer(exam_result).data
#                 result_data.pop("exam", None)  # remove nested exam object
#             else:
#                 result_data = None

#             exam_data["exam_result"] = result_data

#             data.append(exam_data)

#         return data

 

# # MODULE SERIALIZER
# class ExamHistoryModuleSerializer(serializers.ModelSerializer):

#     exams = serializers.SerializerMethodField()
#     total_exams_wt = serializers.FloatField(
#         source="total_weightage_with_exams",
#         read_only=True
#     )

#     total_wt_marks = serializers.SerializerMethodField()
#     total_percentage = serializers.SerializerMethodField()

#     class Meta:
#         model = Module
#         fields = "__all__"

#     # --------------------------
#     # CACHE PER MODULE (IMPORTANT)
#     # --------------------------
#     def get_bundle(self, obj):

#         if not hasattr(self, "_cache"):
#             self._cache = {}

#         if obj.id not in self._cache:

#             self._cache[obj.id] = ModuleExamService.get_module_data(
#                 obj,
#                 self.context["result_map"]
#             )

#         return self._cache[obj.id]

#     # --------------------------
#     # EXAMS LIST
#     # --------------------------
#     def get_exams(self, obj):

#         exam_bundle, _, _ = self.get_bundle(obj)

#         data = []

#         for exam, result in exam_bundle:

#             exam_data = ExamSerializer(exam).data

#             if result:
#                 result_data = ExamResultSerializer(result).data
#                 result_data.pop("exam", None)
#             else:
#                 result_data = None

#             exam_data["exam_result"] = result_data
#             data.append(exam_data)

#         return data

#     # --------------------------
#     # TOTAL WT MARKS
#     # --------------------------
#     def get_total_wt_marks(self, obj):

#         _, wt, _ = self.get_bundle(obj)
#         return round(wt, 2)

#     # --------------------------
#     # TOTAL PERCENTAGE
#     # --------------------------
#     def get_total_percentage(self, obj):

#         _, wt, total = self.get_bundle(obj)

#         if total == 0:
#             return 0

#         return round((wt * 100) / total, 2)

# # ----------------------------
# # Student
# # ----------------------------
# class ExamHistorySampleStudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ["id","user", "student_type","current_unit", "index_no"]

        
# # MAIN HISTORY SERIALIZER (MEMBER LEVEL)
# class ExamHistorySerializer(serializers.ModelSerializer):

#     student_details = SampleStudentSerializer(source="student",read_only=True)

#     modules = serializers.SerializerMethodField()

#     class Meta:
#         model = BatchMembership
#         fields = "__all__"

#     def get_modules(self, obj):

#         modules = Module.objects.filter(
#             batch=obj.batch
#         ).prefetch_related(
#             "module_subjects__exams__subject__weightage_distribution"
#         )

#         exam_results = (
#             ExamResult.objects
#             .filter(membership=obj)
#             .select_related(
#                 "exam",
#                 "exam__subject",
#                 "exam__subject__weightage_distribution",
#             )
#         )

#         result_map = {
#             r.exam_id: r
#             for r in exam_results
#         }

#         return ExamHistoryModuleSerializer(
#             modules,
#             many=True,
#             context={
#                 "result_map": result_map
#             }
#         ).data

class ExamHistoryModuleSerializer(serializers.ModelSerializer):
    exams = serializers.SerializerMethodField()

    total_exams_wt = serializers.FloatField(source="total_weightage_with_exams",read_only=True)

    total_wt_marks = serializers.SerializerMethodField()
    total_percentage = serializers.SerializerMethodField()
    

    class Meta:
        model = Module
        fields = "__all__"


    # --------------------------
    # CACHE PER MODULE (IMPORTANT)
    # --------------------------
    def get_bundle(self, obj):

        if not hasattr(self, "_cache"):
            self._cache = {}

        if obj.id not in self._cache:

            self._cache[obj.id] = ModuleExamService.get_module_data(
                obj,
                self.context["result_map"]
            )

        return self._cache[obj.id]


    # --------------------------
    # TOTAL WT MARKS
    # --------------------------
    def get_total_wt_marks(self, obj):

        _, wt, _ , _ = self.get_bundle(obj)
        return round(wt, 2)

    # --------------------------
    # TOTAL PERCENTAGE
    # --------------------------
    def get_total_percentage(self, obj):
        _, wt, total, total_wt = self.get_bundle(obj)

        try:
            return round((wt * 100) / total_wt, 2)
        except (ZeroDivisionError, TypeError):
            return 0



    def get_exams(self, obj):

        result_map = self.context["result_map"]
        grade_type = self.context.get("grade_type")

        exams = []

        for subject in obj.module_subjects.all():

            qs = subject.exams.all()

            if grade_type and not grade_type == "all":
                qs = qs.filter(grade_type=grade_type)

            exams.extend(qs)

        data = []

        for exam in exams:

            exam_data = ExamSerializer(exam).data

            exam_result = result_map.get(exam.id)

            if exam_result:
                result_data = ExamResultSerializer(exam_result).data
                result_data.pop("exam", None)
            else:
                result_data = None

            exam_data["exam_result"] = result_data

            data.append(exam_data)

        return data





class ExamHistorySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)
    student_rank = serializers.CharField(source="student.user.rank.name", read_only=True)
    student_current_unit = serializers.CharField(source="student.user.current_unit", read_only=True)
    student_personal_number = serializers.CharField(source="student.user.personal_number", read_only=True)

    modules = serializers.SerializerMethodField()

    grade_type_summary = serializers.SerializerMethodField()

    class Meta:
        model = BatchMembership
        fields = "__all__"

    def get_bundle(self, obj):

        if not hasattr(self, "_bundle"):
            self._bundle = {}

        if obj.id not in self._bundle:

            modules = Module.objects.filter(
                batch=obj.batch
            ).prefetch_related(
                "module_subjects__exams"
            )

            exam_results = (
                ExamResult.objects
                .filter(membership=obj)
                .select_related("exam")
            )

            grade_type = self.context.get("grade_type")

            result_map = {}

            for result in exam_results:

                if grade_type and result.exam.grade_type != grade_type:
                    continue

                result_map[result.exam_id] = result

            self._bundle[obj.id] = (modules, result_map)

        return self._bundle[obj.id]

    def get_modules(self, obj):

        modules, result_map = self.get_bundle(obj)

        return ExamHistoryModuleSerializer(
            modules,
            many=True,
            context={
                "membership": obj,
                "result_map": result_map,
                "grade_type": self.context.get("grade_type"),
            },
        ).data

    def get_grade_type_summary(self, obj):

        summary = {}
        modules = Module.objects.filter(batch=obj.batch).prefetch_related("module_subjects__exams")
        memberships = BatchMembership.objects.filter(batch=obj.batch,is_active=True)

        for grade_type, _ in GRADE_TYPE_CHOICES:

            # --------------------------
            # Current Student Data
            # --------------------------
            exam_results = (ExamResult.objects.filter(membership=obj,exam__grade_type=grade_type).select_related("exam"))

            result_map = {
                result.exam_id: result
                for result in exam_results
            }

            obtained_module_wt_marks = 0
            total_module_wt_marks = 0

            for module in modules:

                _, wt, total_full_mark, total_wt_mark = ModuleExamService.get_module_data(module,result_map)

                obtained_module_wt_marks += wt 
                total_module_wt_marks += total_wt_mark

            percentage = 0

            if total_module_wt_marks:
                percentage = round((obtained_module_wt_marks * 100) / total_module_wt_marks,2)
                # percentage = round((obtained_module_wt_marks * total_module_wt_marks) / 100,2)


            # --------------------------
            # Grade
            # --------------------------
            grade_obj = ExamGrade.objects.filter(
                mark_from__lte=percentage,
                mark_to__gte=percentage
            ).first()

            grade = None
            grade_point = None

            if grade_obj:

                grade = (
                    grade_obj.b_side_grade
                    if grade_type == "b_side"
                    else grade_obj.y_side_grade
                )

                grade_point = grade_obj.grade_point

            # --------------------------
            # Merit Position
            # --------------------------
            scores = []

            for membership in memberships:

                membership_results = (ExamResult.objects.filter(membership=membership,exam__grade_type=grade_type).select_related("exam"))

                membership_result_map = {
                    result.exam_id: result
                    for result in membership_results
                }

                obtained = 0
                total = 0

                for module in modules:

                    _, wt, module_total, module_wt_total = ModuleExamService.get_module_data(
                        module,
                        membership_result_map
                    )

                    obtained += wt
                    total += module_total

                member_percentage = 0

                if total:
                    member_percentage = (obtained * 100) / total

                scores.append({
                    "membership_id": membership.id,
                    "percentage": member_percentage,
                })

            scores.sort(
                key=lambda x: x["percentage"],
                reverse=True
            )

            merit_position = None

            for position, score in enumerate(scores, start=1):

                if score["membership_id"] == obj.id:
                    merit_position = position
                    break

            # --------------------------
            # Final Summary
            # --------------------------
            summary[grade_type] = {
                "obtained_module_wt_marks": round(obtained_module_wt_marks,2),
                "total_module_wt_marks": round(total_module_wt_marks,2),
                "percentage": percentage,
                "grade": grade,
                "grade_point": grade_point,
                "merit_position": merit_position,
            }

        return summary