from employee_module.models import Employee
from rest_framework.permissions import BasePermission


class DailyTaskPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if (
            request.method in ["GET"]
            and hasattr(user, "employee")
            and (user.is_superuser
            or user.employee.role == Employee.HR)
        ):
            return True

        if hasattr(user, "employee") and obj.employee == user.employee:
            return True
        return False
