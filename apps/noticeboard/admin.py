from django.contrib import admin

from .models import Event, Notice


# -----------------------------
# Event Admin
# -----------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "event_for",
        "place",
        "from_date",
        "to_date",
        "is_view_on_web",
        "created_at",
    )

    list_filter = (
        "event_for",
        "is_view_on_web",
        "from_date",
        "to_date",
    )

    search_fields = (
        "title",
        "place",
        "note",
    )

    ordering = ("-from_date",)

    autocomplete_fields = (
        "event_for",
    )

    list_editable = (
        "is_view_on_web",
    )


# -----------------------------
# Notice Admin
# -----------------------------
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "notice_for",
        "date",
        "is_view_on_web",
        "created_at",
    )

    list_filter = (
        "notice_for",
        "is_view_on_web",
        "date",
    )

    search_fields = (
        "title",
        "notice",
    )

    ordering = ("-date",)

    autocomplete_fields = (
        "notice_for",
    )

    list_editable = (
        "is_view_on_web",
    )