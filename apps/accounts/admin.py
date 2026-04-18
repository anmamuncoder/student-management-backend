from django.contrib import admin

# Register your models here.
from .models import User, Rank

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)
    

 
@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("code", "name")
    list_filter = ("is_active",)
    ordering = ("order",)