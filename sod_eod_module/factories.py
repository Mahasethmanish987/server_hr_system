import factory
from employee_module.factories import EmployeeFactory
from .models import DailyTask,DailyTaskStatus
class DailyTaskFactory(factory.django.DjangoModelFactory): 

    class Meta: 
        model=DailyTask

    employee=factory.SubFactory(EmployeeFactory)
    task_name=factory.Faker('sentence',nb_words=4)
    task_description=factory.Faker("text",max_nb_chars=100) 
    date=None 
    status = factory.Iterator([
        DailyTaskStatus.PENDING,
        DailyTaskStatus.COMPLETED,
        DailyTaskStatus.CARRY_FORWARD,
    ]) 