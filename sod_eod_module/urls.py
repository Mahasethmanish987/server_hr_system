
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyTaskViewSet 


router = DefaultRouter()
router.register(r'daily-tasks', DailyTaskViewSet, basename='daily-task')

urlpatterns = [
    
    path('', include(router.urls)),
]