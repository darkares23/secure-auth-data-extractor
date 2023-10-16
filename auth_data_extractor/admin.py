# Register your models here.
from django.contrib import admin

from .models import ExtractedData, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at", "updated_at")
    search_fields = ("name", "email")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)


class ExtractedDataAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "data", "input_type", "created_at", "updated_at")
    search_fields = ("user__name", "user__email", "input_type")
    list_filter = ("input_type", "created_at", "updated_at")
    ordering = ("-created_at",)


admin.site.register(User, UserAdmin)
admin.site.register(ExtractedData, ExtractedDataAdmin)
