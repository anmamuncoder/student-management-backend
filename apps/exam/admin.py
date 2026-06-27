from django.contrib import admin

from .models import (
    ExamGrade,
    Exam,
    ExamResult,
)



# Exam Grade Admin
@admin.register(ExamGrade)
class ExamGradeAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "b_side_grade",
        "y_side_grade",
        "grade_point",
        "mark_from",
        "mark_to",
    ]

    search_fields = [
        "b_side_grade",
        "y_side_grade",
    ]

    ordering = [
        "mark_from",
    ]

    list_per_page = 25



# Exam Result Inline

class ExamResultInline(admin.TabularInline):

    model = ExamResult

    extra = 0

    autocomplete_fields = [
        "membership",
    ]

    fields = [
        "membership",
        "status",
        "obtained_marks",
        "remarks",
        "attended_at",
    ]

    readonly_fields = [
        "attended_at",
    ]

    show_change_link = True



# Exam Admin

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "name",
        "subject",
        "get_module",
        "get_batch",
        "exam_date",
        "start_time",
        "end_time",
        "room_no",
        "grade_type",
    ]

    list_filter = [
        "grade_type",
        "exam_date",
        "subject__module__batch",
    ]

    search_fields = [
        "name",
        "subject__name",
        "room_no",
    ]

    ordering = [
        "-exam_date",
        "start_time",
    ]

    autocomplete_fields = [
        "subject",
    ]

    inlines = [
        ExamResultInline,
    ]

    list_per_page = 25

    @admin.display(description="Module")
    def get_module(self, obj):

        if (
            obj.subject
            and obj.subject.module
        ):
            return obj.subject.module.name

        return "-"

    @admin.display(description="Batch")
    def get_batch(self, obj):

        if (
            obj.subject
            and obj.subject.module
            and obj.subject.module.batch
        ):
            return obj.subject.module.batch.name

        return "-"



# Exam Result Admin

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "get_student",
        "get_personal_number",
        "get_batch",
        "get_index_no",
        "exam",
        "status",
        "obtained_marks",
        "attended_at",
    ]

    list_filter = [
        "status",
        "exam",
        "membership__batch",
    ]

    search_fields = [
        "membership__student__user__full_name",
        "membership__student__user__personal_number",
        "exam__name",
    ]

    ordering = [
        "membership__batch__name",
        "membership__index_no",
    ]

    autocomplete_fields = [
        "membership",
        "exam",
    ]

    readonly_fields = [
        "attended_at",
    ]

    list_select_related = [
        "membership",
        "membership__student",
        "membership__student__user",
        "membership__batch",
        "exam",
    ]

    list_per_page = 50

    @admin.display(description="Student")
    def get_student(self, obj):

        if (
            obj.membership
            and obj.membership.student
            and obj.membership.student.user
        ):
            return obj.membership.student.user.full_name

        return "-"

    @admin.display(description="P/Number")
    def get_personal_number(self, obj):

        if (
            obj.membership
            and obj.membership.student
            and obj.membership.student.user
        ):
            return obj.membership.student.user.personal_number

        return "-"

    @admin.display(description="Batch")
    def get_batch(self, obj):

        if (
            obj.membership
            and obj.membership.batch
        ):
            return obj.membership.batch.name

        return "-"

    @admin.display(description="Index No")
    def get_index_no(self, obj):

        if obj.membership:
            return obj.membership.index_no

        return "-"