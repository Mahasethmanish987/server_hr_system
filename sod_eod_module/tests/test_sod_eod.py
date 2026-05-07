import pytest
from sod_eod_module.factories import DailyTaskFactory
from datetime import date 

def test_daily_task_creation(db): 
    task=DailyTaskFactory(date=date.today())
    assert task.id is not None 
    assert task.employee is not None 
    assert task.status is not None 