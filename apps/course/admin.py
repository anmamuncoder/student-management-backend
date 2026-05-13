from django.contrib import admin
from .models import Course, Subject, Module, Syllabus, Batch


# ----------------------------
# INLINES
# ----------------------------
class SyllabusInline(admin.TabularInline):
    model = Syllabus
    extra = 1
    fields = ('module', 'trade', 'note')


class BatchInline(admin.TabularInline):
    model = Batch
    extra = 0
    fields = ('name', 'batch_start', 'batch_end', 'si', 'oic')
    show_change_link = True


# ----------------------------
# COURSE ADMIN
# ----------------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'duration', 'vacancy')
    search_fields = ('name', 'short_name')

    inlines = [SyllabusInline, BatchInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'short_name', 'duration', 'vacancy')
        }),
        ('Notes', {
            'classes': ('collapse',),
            'fields': ('note',)
        }),
    )


# ----------------------------
# SUBJECT ADMIN
# ----------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


# ----------------------------
# MODULE ADMIN
# ----------------------------
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


# ----------------------------
# SYLLABUS ADMIN
# ----------------------------
@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('course', 'module', 'trade')
    list_filter = ('course', 'module')
    search_fields = ('course__name', 'module__name', 'trade')
    list_select_related = ('course', 'module')

 


# ----------------------------
# BATCH ADMIN
# ----------------------------
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'batch_start', 'batch_end', 'si', 'oic', 'main_mark', 'total_mark')
    list_filter = ('course', 'vacation_option')
    search_fields = ('name', 'course__name')
    list_select_related = ('course', 'si', 'oic')

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'course', 'batch_start', 'batch_end', 'vacation_option')
        }),
        ('Staff', {
            'fields': ('si', 'oic')
        }),
        ('Marks', {
            'fields': ('main_mark', 'total_mark')
        }),
        ('Observation Marks', {
            'classes': ('collapse',),
            'fields': (
                'comds_obsn_mks', 'ci_obsn_mks',
                'sis_obsn_mks', 'oics_obsn_mks',
            )
        }),
        ('AFVCF / FTX Options', {
            'classes': ('collapse',),
            'fields': (
                'afvcf_dm', 'afvcf_wrls',
                'ftx_dm', 'ftx_gnry', 'ftx_wrls',
            )
        }),
        ('Notes', {
            'classes': ('collapse',),
            'fields': ('note',)
        }),
    )