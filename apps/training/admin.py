from django.contrib import admin

from .models import (
    TrainingProgramme,
    WeightageDistribution,
    ObservationSheet,
    FinalResult
)


# -----------------------------
# Training Programme
# -----------------------------
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

    ordering = ("-created_at",)

    autocomplete_fields = (
        "course",
        "batch",
    )


# -----------------------------
# Weightage Distribution
# -----------------------------
@admin.register(WeightageDistribution)
class WeightageDistributionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "training_programme",
        "topic",
        "total_marks",
        "practical_marks",
        "theory_marks",
        "percentage",
    )

    list_filter = (
        "course",
        "batch",
        "training_programme",
    )

    search_fields = (
        "topic",
        "training_programme__name",
        "course__name",
    )

    ordering = ("-created_at",)

    autocomplete_fields = (
        "course",
        "batch",
        "training_programme",
    )


# -----------------------------
# Observation Sheet
# -----------------------------
@admin.register(ObservationSheet)
class ObservationSheetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "course",
        "batch",
        "index_no",
        "observation_date",
        "observation_mark",
        "point",
        "observation_by",
    )

    list_filter = (
        "course",
        "batch",
        "observation_date",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__index_no",
    )

    ordering = ("-observation_date",)

    autocomplete_fields = (
        "course",
        "batch",
        "student",
        "observation_by",
    )


# -----------------------------
# Final Result
# -----------------------------
@admin.register(FinalResult)
class FinalResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "course",
        "batch",
        "training_programme",
        "obtained_marks",
        "final_percentage",
        "grade",
        "result_status",
        "published_at",
    )

    list_filter = (
        "course",
        "batch",
        "result_status",
        "grade",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__index_no",
        "grade",
    )

    ordering = ("-published_at",)

    autocomplete_fields = (
        "course",
        "batch",
        "student",
        "training_programme",
        "published_by",
    )