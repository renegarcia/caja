from .models import Movement
from django_tables2 import Table, Column
from django.utils.translation import gettext_lazy as _


class MovementTable(Table):
    cancel_button = Column(
        empty_values=(), verbose_name="", linkify=lambda record: record.get_cancel_url()
    )

    def render_cancel_button(self, record):
        if record.is_canceled():
            return ""
        else:
            return _("Cancelar")

    def render_qty(self, value):
        return f"${value}"

    class Meta:
        model = Movement
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = (
            "date",
            "desc",
            "type",
            "status",
            "qty",
        )
        row_attrs = {
            "class": lambda record: "text-danger" if record.is_canceled() else ""
        }
