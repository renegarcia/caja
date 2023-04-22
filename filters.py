from .models import Movement
from django_filters import FilterSet
import django_filters
from django_filters import widgets
from django.utils.translation import gettext_lazy as _


class MovementFilter(FilterSet):
    date = django_filters.DateFromToRangeFilter(
        widget=widgets.DateRangeWidget(attrs={"type": "date"}),
        label=_("Rango de fechas"),
    )

    class Meta:
        model = Movement
        fields = {
            "desc": ["icontains"],
            "type": ["exact"],
        }
