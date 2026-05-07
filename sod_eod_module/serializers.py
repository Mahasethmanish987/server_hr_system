from rest_framework import serializers 
from .models import DailyTask,DailyTaskStatus
from employee_module.models import Employee 



class DailyTaskSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    status = serializers.ChoiceField(
        choices=DailyTaskStatus.choices,
        required=False,   
        allow_null=True,  
    )
    
    task_description = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,  
    )
    class Meta: 
        model=DailyTask
        fields=['employee','task_name','task_description','status']

class DailyTaskUpdateSerializer(serializers.ModelSerializer):       
      
      class Meta: 
           model=DailyTask
           fields=['status']
      def validate_status(self,value): 
           if value not in [DailyTaskStatus.CARRY_FORWARD,DailyTaskStatus.COMPLETED]: 
                 raise serializers.ValidationError("Status must be either 'completed' or 'carry forward'.")  
             
      def update(self,instance,validated_data): 
             
             for key,value in validated_data.items():
                if hasattr(instance,key):   
                  setattr(instance,key,value)
             instance.save()
             return instance 
             