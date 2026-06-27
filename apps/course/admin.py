from django.contrib import admin
from django.db.models import Count

from .models import (
    Course,
    Batch,
    Module,
    Subject,
    Syllabus,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "short_name",
        "duration",
        "vacancy",
        "total_batches",
        "total_modules",
        "total_subjects",
        "created_at",
    )

    list_filter = (
        "parent",
    )

    search_fields = (
        "name",
        "short_name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            batch_count=Count("batches", distinct=True),
            module_count=Count("batches__module_batches", distinct=True),
            subject_count=Count("batches__batch_subjects", distinct=True),
        )

    def total_batches(self, obj):
        return obj.batch_count

    total_batches.short_description = "Batches"

    def total_modules(self, obj):
        return obj.module_count

    total_modules.short_description = "Modules"

    def total_subjects(self, obj):
        return obj.subject_count

    total_subjects.short_description = "Subjects"


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "course",
        "si",
        "oic",
        "batch_start",
        "batch_end",
        "total_modules",
        "total_subjects",
        "main_mark",
        "total_mark",
    )

    list_filter = (
        "course",
        "vacation_option",
        "batch_start",
        "batch_end",
    )

    search_fields = (
        "name",
        "course__name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            module_count=Count("module_batches", distinct=True),
            subject_count=Count("batch_subjects", distinct=True),
        )

    def total_modules(self, obj):
        return obj.module_count

    total_modules.short_description = "Modules"

    def total_subjects(self, obj):
        return obj.subject_count

    total_subjects.short_description = "Subjects"


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "batch",
        "trade",
        "total_subjects",
        "created_at",
    )

    list_filter = (
        "batch",
        "trade",
    )

    search_fields = (
        "name",
        "code",
        "trade",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            subject_count=Count("module_subjects", distinct=True),
        )

    def total_subjects(self, obj):
        return obj.subject_count

    total_subjects.short_description = "Subjects"


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "batch",
        "module",
        "method",
        "credit",
        "instructor",
        "syllabus_count",
        "created_at",
    )

    list_filter = (
        "method",
        "batch",
        "module",
    )

    search_fields = (
        "name",
        "code",
        "module__name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            syllabus_total=Count("detail_syllabus", distinct=True),
        )

    def syllabus_count(self, obj):
        return obj.syllabus_total

    syllabus_count.short_description = "Syllabus"


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course",
        "batch",
        "module",
        "subject",
        "trade",
        "lecture",
        "practical",
        "written",
        "others",
        "created_at",
    )

    list_filter = (
        "course",
        "batch",
        "module",
        "subject",
    )

    search_fields = (
        "trade",
        "module__name",
        "subject__name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)