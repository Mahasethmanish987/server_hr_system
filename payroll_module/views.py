from django.shortcuts import render
from .serializers import AllowanceSerializer,DeductionSerializer,SalarySerializer,TaxSerializer
# Create your views here.
from employee_module.permissions import check_hr,check_superuser,IsHrOrSuperUser
from rest_framework import viewsets
from .models import Allowance,Deduction
from .permissions import PayrollPermission,SalaryPermission
from .models import  Salary ,Tax

class AllowanceViewSet(viewsets.ModelViewSet): 

    queryset=Allowance.objects.all()
    serializer_class=AllowanceSerializer
    http_method_names=['get','post','put','patch']
    permission_classes=[PayrollPermission]
    def get_queryset(self): 
       user=self.request.user 
       if user.is_superuser or check_hr(self.request):
           return Allowance.objects.all() 
       elif hasattr(user,'employee'): 
           return Allowance.objects.filter(employee=user.employee)
           
    
class DeductionViewSet(viewsets.ModelViewSet): 

    queryset=Deduction.objects.all()
    serializer_class=DeductionSerializer
    http_method_names=['get','post','put','patch']

    def get_queryset(self): 
        user=self.request.user 
        if user.is_superuser or check_hr(self.request):
           return Deduction.objects.all() 
        elif hasattr(user,'employee'): 
           return Deduction.objects.filter(employee=user.employee)


class TaxViewSet(viewsets.ModelViewSet): 
    queryset=Tax.objects.all()
    serializer_class=TaxSerializer
    permission_classes=[IsHrOrSuperUser]
    http_method_names=['get','post','put','patch']
    

class PaymentViewSet(viewsets.ModelViewSet): 
    queryset=Salary.objects.all().order_by('month')
    serializer_class=SalarySerializer
    permission_classes=[SalaryPermission]
    http_method_names=['get','put','patch']

    def get_queryset(self): 
        user=self.request.user 
        if user.is_superuser or check_hr(self.request):
           return Salary.objects.all() 
        elif hasattr(user,'employee'): 
           return Salary.objects.filter(employee=user.employee)
