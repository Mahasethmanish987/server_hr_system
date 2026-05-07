import django_filters

from .models import DailyTask


class DailyTaskFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="employee__username", lookup_expr="icontains"
    )
    date = django_filters.DateFilter(field_name="date", lookup_expr="exact")

    class Meta:
        model = DailyTask
        fields = ["username", "date"]
