from django.shortcuts import render
from .serializers import DailyTaskSerializer,DailyTaskUpdateSerializer
from rest_framework import viewsets
from .models import DailyTask
from .permissions import DailyTaskPermission
from employee_module.models import Employee
from django.db.models import Q 
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status 
from .filters import DailyTaskFilter
from django_filters.rest_framework import DjangoFilterBackend

class DailyTaskViewSet(viewsets.ModelViewSet): 
    queryset=DailyTask.objects.all()
    serializer_class=DailyTaskSerializer
    permission_classes=[DailyTaskPermission]
    http_method_names=['get','post','put','patch']
    filter_backends = [DjangoFilterBackend]
    filterset_class = DailyTaskFilter

    def get_queryset(self):
        user=self.request.user

        if hasattr(user,'employee') and (user.is_superuser or user.employee.role==Employee.HR): 
            return DailyTask.objects.all()
        if hasattr(user,'employee') and user.employee.role==Employee.MANAGER: 
            return DailyTask.objects.filter(Q(employee__reporting_manager=user.employee)|Q(employee=user.employee))
        else: 
            return DailyTask.objects.filter(employee=user.employee)
        
    def get_serializer_class(self):
        if self.action in ['update_status']: 
            return DailyTaskUpdateSerializer
        return DailyTaskSerializer
    @action(detail=True,methods=['patch'],url_path='update-status',permission_classes=[DailyTaskPermission])
    def update_status(self,request,pk=None): 
        daily_task=self.get_object()
        serializer=self.get_serializer(daily_task,data=request.data,context={'request':request},partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        except ValidationError as e: 
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        