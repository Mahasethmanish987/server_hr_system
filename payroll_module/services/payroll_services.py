from datetime import date
from decimal import Decimal

from employee_module.models import Employee
from payroll_module.models import Salary


class PayrollWriteService:
    @staticmethod
    def create_salary(
        employee_id: int,
        salary_year: date,
        salary_month: date,
        basic_salary: Decimal,
        overtime_pay: Decimal,
        tax_amount: Decimal,
        total_allowance_amount: int,
        total_deduction_amount: int,
        allowance_dict: dict,
        deduction_dict: dict,
        net_salary: Decimal,
    ) -> None:
        employee = Employee.objects.get(id=employee_id)

        # create salary object
        salary = Salary.objects.create(
            employee=employee,
            year=salary_year,
            month=salary_month,
            basic_salary=basic_salary,
            overtime_pay=overtime_pay,
            tax_amount=tax_amount,
            allowances_amount=total_allowance_amount,
            deduction_amount=total_deduction_amount,
            net_amount=net_salary,
            paying_structure={
                "allowances": allowance_dict,
                "deductions": deduction_dict,
            },
        )
        return salary

    @staticmethod
    def update_salary(salary_id: id, salary_data: dict) -> Salary:
        salary = Salary.objects.get(id=salary_id)
        if not salary:
            pass

        for key, value in salary_data.items():
            if hasattr(salary, key):
                setattr(salary, key, value)
        net_amount = PayrollWriteService.get_net_amount(
            salary.basic_salary,
            salary.allowances_amount,
            salary.deduction_amount,
            salary.tax_amount,
        )
        salary.net_amount = net_amount
        salary.save()
        return salary

    @staticmethod
    def get_net_amount(basic_salary, allowances, deductions, tax):
        return basic_salary + allowances - deductions - tax


class PayrollReadService:
    def check_salary_exists_for_months(employee_id: id, target_month: date):
        return Salary.objects.filter(
            employee__id=employee_id, month=target_month, year=target_month.year
        ).exists()
