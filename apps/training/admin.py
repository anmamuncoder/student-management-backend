from django.contrib import admin
from .models import (
    TrainingProgramme,
    WeightageDistribution,
    ObservationSheet,
    FinalResult,
)


@admin.register(TrainingProgramme)
class TrainingProgrammeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "course",
        "batch",
        "start_date",
        "end_date",
        "created_at",
    )
    list_filter = (
        "course",
        "batch",
        "start_date",
        "end_date",
    )
    search_fields = (
        "name",
        "code",
        "course__name",
        "batch__name",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)


@admin.register(WeightageDistribution)
class WeightageDistributionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "full_mark",
        "pass_mark",
        "practical_marks",
        "theory_marks",
        "wt",
        "percentage",
        "observation_by",
    )
    list_filter = (
        "subject",
        "observation_by",
    )
    search_fields = (
        "subject__name",
        "topic",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)


@admin.register(ObservationSheet)
class ObservationSheetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "course",
        "batch",
        "index_no",
        "observation_date",
        "observation_time",
        "observation_mark",
        "point",
        "observation_by",
    )
    list_filter = (
        "course",
        "batch",
        "observation_date",
        "observation_by",
    )
    search_fields = (
        "student__name",
        "student__student_id",
        "remark",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)


@admin.register(FinalResult)
class FinalResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "course",
        "batch",
        "training_programme",
        "obtained_marks",
        "total_marks",
        "final_percentage",
        "grade",
        "result_status",
        "published_by",
        "published_at",
    )
    list_filter = (
        "course",
        "batch",
        "training_programme",
        "result_status",
        "published_at",
    )
    search_fields = (
        "student__name",
        "student__student_id",
        "grade",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "published_at",
    )
    ordering = ("-created_at",)