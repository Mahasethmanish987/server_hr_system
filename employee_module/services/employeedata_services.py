import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import DatabaseError, IntegrityError, transaction
from employee_module.models import Department, Employee

logger = logging.getLogger(__name__)


class EmployeeDataService:
    @staticmethod
    def get_employee_payment_detail(employee_id: id) -> dict:
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValidationError("Invalid employee ID")
        employee = (
            Employee.objects.filter(id=employee_id)
            .prefetch_related("overtime_rate")
            .first()
        )
        if not employee:
            raise ObjectDoesNotExist(f"No employee found for ID {employee_id}")
        overtime_hour_rate = 0
        if (
            hasattr(employee, "overtime_rate")
            and employee.overtime_rate.overtime_rate is not None
        ):
            overtime_hour_rate = employee.overtime_rate.overtime_rate

        return {
            "overtime_hour_rate": overtime_hour_rate,
            "salary": employee.current_salary,
            "marital_status": employee.marital_status,
        }

    @staticmethod
    def get_all_employee_ids() -> list[int]:
        return list(
            Employee.objects.filter(is_active=True).values_list("id", flat=True)
        )

    @staticmethod
    def get_employees_without_salary(target_month, target_year) -> list[int]:
        return list(
            Employee.objects.filter(is_active=True)
            .exclude(salary__month=target_month, salary__year=target_year)
            .values_list("id", flat=True)
        )


class EmployeeWriteService:
    @staticmethod
    def update(employee_id: id, validated_data: dict) -> Employee:
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValidationError(f"Invalid employee ID{employee_id}")

        employee = Employee.objects.filter(id=employee_id).first()
        if not employee:
            raise ObjectDoesNotExist(f"No employee found for ID {employee_id}")

        user = validated_data.pop("user", None)
        try:
            with transaction.atomic():
                if user:
                    updated_user = UserWriteService.update(employee.user.id, user)
                    employee.user = updated_user

                for key, value in validated_data.items():
                    if hasattr(employee, key):
                        setattr(employee, key, value)

                employee.save()
                return employee
        except IntegrityError as e:
            raise IntegrityError(
                f"Employee update failed due to data integrity issues {employee.id} for {e}"
            )

        except DatabaseError as e:
            raise DatabaseError(
                f"Unable to update Employee due to database error{employee.id} for {e}"
            )

        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist(
                f"No Employee found for ID {employee.user.id} for {e}"
            )

        except Exception as e:
            raise ValidationError(f"Employee update failed{employee.user.id} for {e}")


User = get_user_model()


class UserWriteService:
    @staticmethod
    def update(user_id, validated_data: dict):
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationError(f"Invalid user ID {user_id}")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f"No user found for ID {user_id}")
        try:
            with transaction.atomic():
                for key, value in validated_data.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                user.save()
                return user
        except IntegrityError as e:
            raise IntegrityError(
                f"User update failed due to data integrity issues for {user_id} for {e}"
            )

        except DatabaseError as e:
            raise DatabaseError(
                f"Unable to update user due to database error for {user_id} for {e}"
            )

        except Exception as e:
            raise ValidationError(f"User update failed for {user_id} for {e}")

    @staticmethod
    def create_user(validated_data: dict) -> User:
        if isinstance(validated_data, dict) is False:
            raise ValidationError("Invalid data format")

        password = validated_data.pop("password", None)
        if not password:
            raise ValidationError("Password is required")
        try:
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user

        except IntegrityError as e:
            raise IntegrityError(
                f"User creation failed due to data integrity issues {e}"
            )

        except DatabaseError as e:
            raise DatabaseError(f"Unable to create user due to database error for {e}")

        except Exception as e:
            raise ValidationError(f"User creation failed for {e}")


class DepartmentReadService:
    @staticmethod
    def check_existing_manager(employee_id: id) -> bool:
        if Department.objects.filter(manager__id=employee_id).exists():
            return True
        return False
