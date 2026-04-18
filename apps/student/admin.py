from django.contrib import admin
from .models import (
    Student, StudentType, StudentGroup, Activity,
    Spouse, Qualification, BankAccount, MilitaryQualification,
    ServiceRecord, Award, UNMission, CountryVisited
)


# ----------------------------
# INLINES
# ----------------------------
class SpouseInline(admin.TabularInline):
    model = Spouse
    extra = 1
    fields = ('spouse_name', 'spouse_phone', 'spouse_profession', 'spouse_address')


class QualificationInline(admin.TabularInline):
    model = Qualification
    extra = 1
    fields = ('name', 'qualification_type', 'institute', 'from_date', 'to_date', 'result')


class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 1
    fields = ('bank_name', 'account_number', 'branch')


class MilitaryQualificationInline(admin.TabularInline):
    model = MilitaryQualification
    extra = 1
    fields = ('cadre_name', 'level', 'institute', 'duration_from', 'duration_to', 'result')


class ServiceRecordInline(admin.TabularInline):
    model = ServiceRecord
    extra = 1
    fields = ('institution', 'appointment', 'from_date', 'to_date')


# ----------------------------
# STUDENT ADMIN
# ----------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'student_type', 'is_active','index_no','date_of_joining_accs')
    list_filter = ('is_active', 'student_type','batch')
    search_fields = ('user__full_name', 'user__email', 'passport_number',)
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('user', 'student_type')

    inlines = [
        SpouseInline,
        QualificationInline,
        BankAccountInline,
        MilitaryQualificationInline,
        ServiceRecordInline,
    ]

    fieldsets = (
        ('User', {
            'fields': ('user', 'is_active')
        }),
        ('Academic Info', {
            'fields': (
                'student_type', 
                'batch',
                'index_no',
                'second_language',
                'date_of_commission', 'date_of_joining_accs',
            )
        }),
        ('Father Information', {
            'classes': ('collapse',),
            'fields': (
                'father_full_name', 'father_phone',
                'father_profession', 'father_address',
            )
        }),
        ('Mother Information', {
            'classes': ('collapse',),
            'fields': (
                'mother_full_name', 'mother_phone',
                'mother_profession', 'mother_address',
            )
        }),
        ('Passport', {
            'classes': ('collapse',),
            'fields': (
                'passport_number', 'passport_issue_date',
                'passport_place', 'passport_expiry_date',
            )
        }),
        ('Health & Other', {
            'classes': ('collapse',),
            'fields': ('health_condition', 'other_info')
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description='Full Name')
    def get_full_name(self, obj):
        return obj.user.full_name

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email


# ----------------------------
# STUDENT TYPE ADMIN
# ----------------------------
@admin.register(StudentType)
class StudentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ----------------------------
# STUDENT GROUP ADMIN
# ----------------------------
@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ----------------------------
# ACTIVITY ADMIN
# ----------------------------
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'batch', 'activity_date')
    list_filter = ('course', 'batch', 'activity_date')
    search_fields = ('student__user__full_name',)
    date_hierarchy = 'activity_date'
    list_select_related = ('student', 'course', 'batch')


# ----------------------------
# QUALIFICATION ADMIN
# ----------------------------
@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'qualification_type', 'institute', 'from_date', 'to_date', 'result')
    list_filter = ('qualification_type',)
    search_fields = ('student__user__full_name', 'name', 'institute')
    list_select_related = ('student',)


# ----------------------------
# MILITARY QUALIFICATION ADMIN
# ----------------------------
@admin.register(MilitaryQualification)
class MilitaryQualificationAdmin(admin.ModelAdmin):
    list_display = ('cadre_name', 'student', 'level', 'institute', 'duration_from', 'duration_to', 'result')
    search_fields = ('student__user__full_name', 'cadre_name')
    list_select_related = ('student',)


# ----------------------------
# BANK ACCOUNT ADMIN
# ----------------------------
@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'branch', 'student')
    search_fields = ('student__user__full_name', 'bank_name', 'account_number')
    list_select_related = ('student',)


# ----------------------------
# SERVICE RECORD ADMIN
# ----------------------------
@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'institution', 'appointment', 'from_date', 'to_date')
    search_fields = ('student__user__full_name', 'institution')
    list_select_related = ('student',)


# ----------------------------
# AWARD ADMIN
# ----------------------------
@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('decoration', 'receipt_date', 'purpose')
    search_fields = ('decoration',)
    date_hierarchy = 'receipt_date'


# ----------------------------
# UN MISSION ADMIN
# ----------------------------
@admin.register(UNMission)
class UNMissionAdmin(admin.ModelAdmin):
    list_display = ('mission_name', 'country', 'appointment', 'from_date', 'to_date')
    list_filter = ('country',)
    search_fields = ('mission_name', 'country', 'appointment')


# ----------------------------
# COUNTRY VISITED ADMIN
# ----------------------------
@admin.register(CountryVisited)
class CountryVisitedAdmin(admin.ModelAdmin):
    list_display = ('country', 'from_date', 'to_date', 'purpose')
    list_filter = ('country',)
    search_fields = ('country',)
    date_hierarchy = 'from_date'