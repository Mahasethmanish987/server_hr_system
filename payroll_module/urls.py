from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaxViewSet, AllowanceViewSet, DeductionViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'taxes', TaxViewSet, basename="tax")
router.register(r'allowances', AllowanceViewSet, basename="allowance")
router.register(r'deductions', DeductionViewSet, basename="deduction")
router.register(r'payments', PaymentViewSet, basename="payment")

app_name = "payroll"

urlpatterns = [
    path("", include(router.urls)),
]