from rest_framework.permissions import BasePermission
from rest_framework import permissions 
from employee_module.permissions import check_hr,check_superuser

class PayrollPermission(BasePermission): 

    def has_permission(self, request, view):
        user=request.user 

        if not request.user.is_authenticated: 
            return False 
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        if request.method in ["POST","PUT","PATCH"]: 
            return user.is_superuser or check_hr(request)
        return False 
    

class SalaryPermission(BasePermission): 


    def has_permission(self, request, view):
        user=request.user 
        if not request.user.is_authenticated: 
          return False 

        if request.method in permissions.SAFE_METHODS: 
            return True 
        if request.method in ["PUT","PATCH"]: 
            return user.is_superuser or check_hr(request)
        return False 
    
    def has_object_permission(self, request, view, obj):
        user=request.user 
        if request.method in ['PUT','PATCH']: 
            return user.is_superuser or check_hr(request)
        if request.method in permissions.SAFE_METHODS: 
            return True 
        return False 