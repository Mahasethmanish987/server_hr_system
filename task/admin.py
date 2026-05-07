from django.contrib import admin
from .models import Task, SubTask
from .models import OnboardingOffboardingTask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "assigned_by",
        "assigned_to",
        "status",
        "priority",
        "due_date",
        "department",
        "created_at",
    )
    list_filter = ("status", "priority", "department", "due_date")
    search_fields = ("title", "description", "assigned_by__user__username", "assigned_to__user__username")
    ordering = ("-created_at",)
    date_hierarchy = "due_date"

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "parent_task",
        "assigned_by",
        "assigned_to",
        "status",
        "priority",
        "due_date",
        "department",
        "created_at",
    )
    list_filter = ("status", "priority", "department", "due_date")
    search_fields = (
        "title",
        "description",
        "parent_task__title",
        "assigned_by__user__username",
        "assigned_to__user__username",
    )
    ordering = ("-created_at",)
    date_hierarchy = "due_date"

@admin.register(OnboardingOffboardingTask)
class OnboardingOffboardingTaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_name",
        "task_type",
        "department",
        "job_title",
        "applies_to_all",
        "made_by",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "task_type",
        "department",
        "job_title",
        "applies_to_all",
    )

    search_fields = (
        "task_name",
        "department__name",
        "job_title__title",
        "made_by__user__username",
    )

    autocomplete_fields = (
        "department",
        "job_title",
        "made_by",
    )

    list_editable = (
        "task_type",
        "department",
        "job_title",
        "applies_to_all",
    )

    ordering = ("-created_at",)