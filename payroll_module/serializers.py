from django.utils import timezone
from employee_module.models import Employee
from rest_framework import serializers

from payroll_module.services.payroll_services import PayrollWriteService

from .models import Allowance, Deduction, Salary, Tax


class AllowanceSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Allowance
        fields = ["employee", "allowance_type", "amount"]

    def create(self, validated_data):
        month = timezone.localdate()
        allowance = Allowance.objects.create(**validated_data, month=month)
        return allowance


class DeductionSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Deduction
        fields = ["employee", "type", "amount"]

    def create(self, validated_data):
        month = timezone.localdate()
        deduction = Deduction.objects.create(**validated_data, month=month)
        return deduction


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = [
            "tax_name",
            "tax_percentage",
            "starting_salary",
            "ending_salary",
            "taxpayer_type",
        ]



class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = [
            "basic_salary",
            "overtime_pay",
            "tax_amount",
            "allowances_amount",
            "deduction_amount",
            "net_amount",
        ]

    def update(self, instance, validated_data):
        salary = PayrollWriteService.update_salary(instance.id, validated_data)
        return salary
