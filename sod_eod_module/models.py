from django.db import models
from employee_module.models import Employee, TimeStamp
from datetime import date 


class DailyTaskStatus(models.TextChoices): 
      PENDING='pending','Pending'
      COMPLETED='completed','Completed'
      CARRY_FORWARD='carry_forward','Carry Forward'
    

class DailyTask(TimeStamp):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="daily_task",
    )
    task_name=models.CharField(max_length=255)
    task_description=models.TextField(blank=True,null=True)
    date=models.DateField(default=date.today)
    status=models.CharField(choices=DailyTaskStatus,max_length=30,default=DailyTaskStatus.PENDING)

