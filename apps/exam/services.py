from apps.student.models import BatchMembership
from .models import ExamResult, Exam, ExamGrade
from .constants import AttendanceStatus 
from apps.course.models import Module

# Create ExamResult Automatically
def create_exam_result(exam):

    batch = exam.batch

    if not batch:
        return

    memberships = BatchMembership.objects.filter(
        batch=batch,
        is_active=True
    )

    result_objects = []

    for membership in memberships:

        result_objects.append(
            ExamResult(
                membership=membership,
                exam=exam,
                status=AttendanceStatus.PENDING,
                obtained_marks=0
            )
        )

    ExamResult.objects.bulk_create(
        result_objects,
        ignore_conflicts=True
    )

    return True
 

class ModuleExamService:

    @staticmethod
    def get_module_data(module, result_map):

        exams = Exam.objects.filter(
            subject__module=module
        ).select_related(
            "subject__weightage_distribution",
            "subject"
        ).distinct()

        total_wt_marks = 0
        total_full_marks = 0
        obtained_wt_full_marks = 0


        exam_bundle = []

        for exam in exams:

            result = result_map.get(exam.id)

            wd = getattr(exam.subject, "weightage_distribution", None)

            if wd:
                total_full_marks += wd.full_mark or 0

            if result:
                total_wt_marks +=  result.wt or 0
                obtained_wt_full_marks += result.wt_marks or 0

            exam_bundle.append((exam, result))

        return exam_bundle, obtained_wt_full_marks, total_full_marks, total_wt_marks